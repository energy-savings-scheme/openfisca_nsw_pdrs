import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_core.parameters import load_parameter_file

class motor_poles_number(Enum):
    poles_2="poles_2"
    poles_4="poles_4"
    poles_6="poles_6"
    poles_8="poles_8"



class PDRS__motors__number_of_poles(Variable):
    entity=Building
    value_type=Enum
    possible_values=motor_poles_number
    default_value=motor_poles_number.poles_8
    definition_period=ETERNITY
    reference="Clause **"
    label="How many poles does your new motor have?"
    metadata ={
        'alias' : "New Motor Poles Number ",
        'activity-group' : "High Efficiency Appliances for Business",
        'activity-name' : "Replace an existing motor by a high efficiency motor",
        'variable-type' : "input"
    }




class PDRS__motors__rated_output(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the Rated Output of the old motor being replaced in kW as found in the GEMS Registry"
    metadata={
        "variable-type": "input",
        "alias" :"Rated Output of The New Motor",
        "activity-group":"High Efficiency Appliances for Business",
        "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        }


class PDRS__motors__baseline_motor_efficiency(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="Baseline Motor Efficiency "
    metadata={
        "variable-type": "intermediary",
        "alias" :"Baseline Motor Efficiency",
        "activity-group":"High Efficiency Appliances for Business",
        "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        }

    def formula(building, period, parameters):
        rated_output = building('PDRS__motors__rated_output', period)
        poles = building('PDRS__motors__number_of_poles', period)
        #access the thresholds and amounts in parameters
        data = load_parameter_file("openfisca_nsw_pdrs/parameters/motors/motors_baseline_efficiency_table.yaml")

        output_threshold = []



        poles_str_list = poles.decode_to_str()

        # prison break for parameters
        for parameterAtInstance in data.children['rated_output'].values_list:
            output_threshold.append(parameterAtInstance.value)

        #this should be a matrix now with each poles value
        baselineEfficiencyMatrix = []
        for item in poles_str_list:
            baselineEfficiency = []
            for parameterAtInstance in data.children[poles_str_list[0]].values_list:
                baselineEfficiency.append(parameterAtInstance.value)

            baselineEfficiencyMatrix.append(baselineEfficiency)

        baseline_nparray = np.array(baselineEfficiencyMatrix)

        #compute gradients
        delta_y_matrix = (baseline_nparray[:, 1:]-baseline_nparray[:, :-1])

        delta_y = np.delete(baselineEfficiency, 0) - baselineEfficiency[:-1]
        delta_x = np.delete(output_threshold,0)-output_threshold[:-1]
        gradient_matrix = delta_y_matrix/delta_x
        print(gradient_matrix.shape)
        x_zip = zip(range(len(output_threshold)-1),output_threshold[:-1], np.delete(output_threshold,0))

        #find out which bracket does the user input belong to
        condList = []

        for (index, z1, z2) in x_zip:
            bracket_pos=(rated_output >= z1) * (rated_output < z2)
            condList.append(bracket_pos)

        x_lowerbound = np.select(np.array(condList), output_threshold[:-1])
        y_minus = np.select(np.array(condList), baseline_nparray[:, :-1].T)
        gradient_selected = np.select(np.array(condList), gradient_matrix.T)


        return y_minus + gradient_selected*(rated_output-x_lowerbound)







class PDRS__motors__peak_demand_savings(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="The Peak demand savings "
    metadata={
        "variable-type": "output",
        "alias" :"Motors Peak demand savings",
        "activity-group":"High Efficiency Appliances for Business",
        "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        }

    def formula(building, period, parameters):
        rated_output = building('PDRS__motors__rated_output', period)
        asset_life_table=parameters(period).motors.motors_asset_life_table
        forward_creation_period=asset_life_table.calc(rated_output, right=False)

        return forward_creation_period