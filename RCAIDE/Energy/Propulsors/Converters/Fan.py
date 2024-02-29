## @ingroup Energy-Propulsors-Converters
# RCAIDE/Energy/Propulsors/Converters/Fan.py
# 
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Energy.Energy_Component                      import Energy_Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Fan Component
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Propulsors-Converters
class Fan(Energy_Component):
    """This is a fan component typically used in a turbofan.
    Calling this class calls the compute function.
    
    Assumptions:
    Pressure ratio and efficiency do not change with varying conditions.

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """         
        #set the default values
        self.tag                            = 'Fan'
        self.polytropic_efficiency          = 1.0
        self.pressure_ratio                 = 1.0
        self.angular_velocity               = 0   
        self.inputs.stagnation_temperature  = 0.
        self.inputs.stagnation_pressure     = 0.
        self.outputs.stagnation_temperature = 0.
        self.outputs.stagnation_pressure    = 0.
        self.outputs.stagnation_enthalpy    = 0.