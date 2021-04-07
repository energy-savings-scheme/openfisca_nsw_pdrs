from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

class PDRS__Air_Conditioner__power_input(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the measured full capacity power input at 35C as recorded in the GEMS register?"
    metadata={
        "variable-type": "input",
        "alias" :"AC power input",
        "activity-group":"PDRS: Air Conditioner",
        "activity-name":"Installation or Replacement of an Air Conditioner"
        }


class PDRS__Air_Conditioner__peak_demand_savings(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="The final peak demand savings from the air conditioner"
    metadata={
        "variable-type": "output",
        "alias" :"AC Peak Demand Savings",
        "activity-group":"PDRS: Air Conditioner",
        "activity-name":"Installation or Replacement of an Air Conditioner"
        }

    def formula(building, period, parameters):
        power_input = building('PDRS__Air_Conditioner__power_input', period)
        baseline_power_input = building('PDRS__Air_Conditioner__baseline_power_input', period)
        firmness_factor = building('PDRS__Air_Conditioner__firmness_factor', period)
        daily_peak_hours = parameters(period).PDRS_wide_constants.DAILY_PEAK_WINDOW_HOURS
        forward_creation_period=parameters(period).AC.AC_related_constants.FORWARD_CREATION_PERIOD


        return (baseline_power_input-power_input)*daily_peak_hours*firmness_factor*forward_creation_period
