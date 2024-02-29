## @defgroup Energy-Networks Networks
# RCAIDE/Energy/Networks/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Components.Energy.Networks import Battery_Ducted_Fan                           as legacy_battery_ducted_fan
from Legacy.trunk.S.Components.Energy.Networks import Ducted_Fan                                   as legacy_ducted_fan 
from Legacy.trunk.S.Components.Energy.Networks import Liquid_Rocket                                as legacy_liquid_rocket
from Legacy.trunk.S.Components.Energy.Networks import Propulsor_Surrogate                          as legacy_propulsor_surrogate
from Legacy.trunk.S.Components.Energy.Networks import PyCycle                                      as legacy_pycycle
from Legacy.trunk.S.Components.Energy.Networks import Ramjet                                       as legacy_ramjet
from Legacy.trunk.S.Components.Energy.Networks import Scramjet                                     as legacy_scramjet
from Legacy.trunk.S.Components.Energy.Networks import Serial_Hybrid_Ducted_Fan                     as legacy_serial_hybrid_ducted_fan 
from Legacy.trunk.S.Components.Energy.Networks import Solar_Low_Fidelity                           as legacy_solar_low_fidelity
from Legacy.trunk.S.Components.Energy.Networks import Turboelectric_HTS_Ducted_Fan                 as legacy_turboelectric_hts_ducted_fan
from Legacy.trunk.S.Components.Energy.Networks import Turboelectric_HTS_Dynamo_Ducted_Fan          as legacy_turboelectric_hts_dynamo_ducted_fan
from Legacy.trunk.S.Components.Energy.Networks import Turbofan                                     as legacy_turbofan
from Legacy.trunk.S.Components.Energy.Networks import Turbojet_Super                               as legacy_turbojet
from Legacy.trunk.S.Components.Energy.Networks import Solar                                        as legacy_solar

from .                                                   import Distribution   
from .All_Electric_Network                               import All_Electric_Network 
from .Internal_Combustion_Engine_Network                 import Internal_Combustion_Engine_Network
from .Constant_Speed_Internal_Combustion_Engine_Network  import Constant_Speed_Internal_Combustion_Engine_Network  
from .Isolated_Battery_Cell_Network                      import Isolated_Battery_Cell_Network  
from .Turbofan_Engine_Network                            import Turbofan_Engine_Network
from .Turbojet_Engine_Network                            import Turbojet_Engine_Network 
from .Network                                            import Network  