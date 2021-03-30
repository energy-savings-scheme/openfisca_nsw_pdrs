from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


# smotors_peak_demand_savings

# new_efficiency

# old_efficienty (contains all the estimation logic)



class PDRS__motors__old_rated_output(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the Rated Output of the old motor being replaced in kW as found in the GEMS Registry"
    metadata={
        "variable-type": "input",
        "alias" :"Motors Old Rated Output",
        "activity-group":"",
        "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        }

class PDRS__motors__new_rated_output(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the Rated Output of the old motor being replaced in kW as found in the GEMS Registry"
    metadata={
        "variable-type": "input",
        "alias" :"Motors Old Rated Output",
        "activity-group":"",
        "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        }