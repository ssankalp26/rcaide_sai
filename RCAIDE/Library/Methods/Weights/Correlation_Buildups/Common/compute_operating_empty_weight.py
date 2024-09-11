# RCAIDE/Methods/Weights/Correlation_Buildups/Common/operating_empty_weight.py
# 
# Created: Sep 2024, M. Clarke 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core import Data ,  Units 
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Propulsion as Propulsion 
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Common    as  Common
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Raymer    as  Raymer 
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import FLOPS     as  FLOPS 
from RCAIDE.Library.Methods.Weights.Correlation_Buildups import Transport as  Transport  
from RCAIDE.Library.Attributes.Materials.Aluminum import Aluminum

# python imports 
import numpy as np


# ---------------------------------------------------------------------------------------------------------------------- 
# Operating Empty Weight 
# ----------------------------------------------------------------------------------------------------------------------
def compute_operating_empty_weight(vehicle,settings=None, method_type='RCAIDE', update_fuel_mass = True):
    """ Main function that estimates the zero-fuel weight of a transport aircraft:
        - MTOW = WZFW + FUEL
        - WZFW = WOE + WPAYLOAD
        - WOE = WE + WOPERATING_ITEMS
        - WE = WSTRCT + WPROP + WSYS
        Assumptions:
            1) All nacelles are identical
            2) The number of nacelles is the same as the number of engines 

        Source:
            FLOPS method: The Flight Optimization System Weight Estimation Method
            RCAIDE method: http://aerodesign.stanford.edu/aircraftdesign/AircraftDesign.html
            RAYMER method: Aircraft Design A Conceptual Approach
       Inputs:
            vehicle - data dictionary with vehicle properties               [dimensionless]
                -.networks: data dictionary with all the network elements and properties
                    -.total_weight: total weight of the propulsion system   [kg] 
                      (optional, calculated if not included)
                -.fuselages: data dictionary with the fuselage properties of the vehicle
                -.wings: data dictionary with all the wing properties of the vehicle, including horzinotal and vertical stabilizers
                -.wings['main_wing']: data dictionary with main wing properties
                    -.flap_ratio: flap surface area over wing surface area
                -.mass_properties: data dictionary with all the main mass properties of the vehicle including MTOW, ZFW, EW and OEW

            settings.weight_reduction_factors.
                    main_wing                                               [dimensionless] (.1 is a 10% weight reduction)
                    empennage                                               [dimensionless] (.1 is a 10% weight reduction)
                    fuselage                                                [dimensionless] (.1 is a 10% weight reduction)
            method_type - weight estimation method chosen, available:
                            - FLOPS Simple
                            - FLOPS Complex
                            - RCAIDE 
                            - Raymer
       Outputs:
            output - data dictionary with the weight breakdown of the vehicle
                        -.structures: structural weight
                            -.wing: wing weight
                            -.horizontal_tail: horizontal tail weight
                            -.vertical_tail: vertical tail weight
                            -.fuselage: fuselage weight
                            -.main_landing_gear: main landing gear weight
                            -.nose_landing_gear: nose landing gear weight
                            -.nacelle: nacelle weight
                            -.paint: paint weight
                            -.total: total strucural weight

                        -.propulsion_breakdown: propulsive system weight
                            -.engines: dry engine weight
                            -.thrust_reversers: thrust reversers weight
                            -.miscellaneous: miscellaneous items includes electrical system for engines and starter engine
                            -.fuel_system: fuel system weight
                            -.total: total propulsive system weight

                        -.systems_breakdown: system weight
                            -.control_systems: control system weight
                            -.apu: apu weight
                            -.electrical: electrical system weight
                            -.avionics: avionics weight
                            -.hydraulics: hydraulics and pneumatic system weight
                            -.furnish: furnishing weight
                            -.air_conditioner: air conditioner weight
                            -.instruments: instrumentation weight
                            -.anti_ice: anti ice system weight
                            -.total: total system weight

                        -.payload_breakdown: payload weight
                            -.passengers: passenger weight
                            -.bagage: baggage weight
                            -.cargo: cargo weight
                            -.total: total payload weight

                        -.operational_items: operational items weight
                            -.operating_items_less_crew: unusable fuel, engine oil, passenger service weight and cargo containers
                            -.flight_crew: flight crew weight
                            -.flight_attendants: flight attendants weight
                            -.total: total operating items weight

                        -.empty = structures.total + propulsion_breakdown.total + systems_breakdown.total
                        -.operating_empty = empty + operational_items.total
                        -.zero_fuel_weight = operating_empty + payload_breakdown.total
                        -.fuel = vehicle.mass_properties.max_takeoff - zero_fuel_weight


        Properties Used:
            N/A
    """
    # unpack
    wt_factors = settings.weight_reduction_factors      
    
    Wings = RCAIDE.Library.Components.Wings  
    if method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
        if vehicle.flight_envelope == None:
            raise ValueError("FLOPS requires a design mach number for sizing!")
        if vehicle.flight_envelope.design_range  == None:
            raise ValueError("FLOPS requires a design range for sizing!")
        if vehicle.flight_envelope.design_cruise_altitude == None:
            raise ValueError("FLOPS requires a cruise altitude for sizing!")
        if not hasattr(vehicle, 'flap_ratio'):
            if vehicle.systems.accessories == "sst":
                flap_ratio = 0.22
            else:
                flap_ratio = 0.33
            for wing in vehicle.wings:
                if isinstance(wing, Wings.Main_Wing):
                    wing.flap_ratio = flap_ratio 

    # Payload Weight
    if method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
        payload = FLOPS.compute_payload_weight(vehicle)
    else:
        payload = Common.compute_payload_weight(vehicle)
    
    
    vehicle.payload.passengers                      = RCAIDE.Library.Components.Component()
    vehicle.payload.passengers.mass_properties.mass = payload.passengers
    
    vehicle.payload.baggage                         = RCAIDE.Library.Components.Component()
    vehicle.payload.baggage.mass_properties.mass    = payload.baggage
    
    vehicle.payload.cargo                           = RCAIDE.Library.Components.Component() 
    vehicle.payload.cargo.mass_properties.mass      = payload.cargo    

    ##-------------------------------------------------------------------------------             
    # Operating Items Weight
    ##------------------------------------------------------------------------------- 
    if method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
        wt_oper = FLOPS.compute_operating_items_weight(vehicle)
    else:
        wt_oper = Transport.compute_operating_items_weight(vehicle)  

    ##-------------------------------------------------------------------------------         
    # System Weight
    ##------------------------------------------------------------------------------- 
    if method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
        wt_sys = FLOPS.compute_systems_weight(vehicle)
    elif method_type == 'Raymer':
        wt_sys = Raymer.compute_systems_weight(vehicle)
    else:
        wt_sys = Common.compute_systems_weight(vehicle)
    for item in wt_sys.keys():
        wt_sys[item] *= (1. - wt_factors.systems)
    
    ##-------------------------------------------------------------------------------                 
    # Propulsion Weight 
    ##------------------------------------------------------------------------------- 
    output.propulsion_breakdown = Data() 
    output.propulsion_breakdown.total               = 0
    output.propulsion_breakdown.engines             = 0
    output.propulsion_breakdown.thrust_reversers    = 0
    output.propulsion_breakdown.miscellaneous       = 0
    output.propulsion_breakdown.fuel_system         = 0

    W_energy_network_total              = 0 
    W_energy_network                    = Data()  
    W_energy_network.wt_eng             = 0 
    W_energy_network.wt_thrust_reverser = 0 
    W_energy_network.wt_engine_controls = 0 
    W_energy_network.wt_starter         = 0 
    W_energy_network.fuel_system        = 0 
    W_energy_network.motors             = 0 
    W_energy_network.nacelle            = 0 
    network_number_of_engines           = 0  
    
    network_number_of_engines =  0
    for network in vehicle.networks: 
        # Fuel-Powered Propulsors  
        if method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
            W_energy_network                     = FLOPS.compute_propulsion_system_weight(vehicle, network)
            W_energy_network_total              += W_energy_network.wt_prop 
            W_energy_network.wt_eng             += W_energy_network.wt_eng
            W_energy_network.wt_thrust_reverser += W_energy_network.wt_thrust_reverser
            W_energy_network.wt_engine_controls += W_energy_network.wt_engine_controls
            W_energy_network.wt_starter         += W_energy_network.wt_starter
            W_energy_network.fuel_system        += W_energy_network.fuel_system 
            W_energy_network.nacelle            += W_energy_network.nacelle    
            network_number_of_engines           += W_energy_network.number_of_engines
            
        elif method_type == 'Raymer':
            W_energy_network                    = Raymer.compute_propulsion_system_weight(vehicle, network) 
            W_energy_network_total              += W_energy_network.wt_prop 
            W_energy_network.wt_eng             += W_energy_network.wt_eng
            W_energy_network.wt_thrust_reverser += W_energy_network.wt_thrust_reverser
            W_energy_network.wt_engine_controls += W_energy_network.wt_engine_controls
            W_energy_network.wt_starter         += W_energy_network.wt_starter
            W_energy_network.fuel_system        += W_energy_network.fuel_system 
            W_energy_network.nacelle            += W_energy_network.nacelle    
            network_number_of_engines           += W_energy_network.number_of_engines 
        else:
            for fuel_line in  network.fuel_lines: 
                for propulsor in fuel_line.propulsors:
                    if isinstance(propulsor, RCAIDE.Library.Components.Propulsors.Turbofan):
                        thrust_sls  = propulsor.sealevel_static_thrust  
                        wt_engine_jet = Propulsion.compute_jet_engine_weight(thrust_sls)
                        W_energy_network_total  += Propulsion.integrated_propulsion(wt_engine_jet) 
                        network_number_of_engines += 1             
                 
        # Electric-Powered Propulsors  
        for bus in network.busses: 
            # electrical payload 
            wt_sys.wt_elec  += bus.payload.mass_properties.mass * Units.kg
     
            # Avionics Weight 
            wt_sys.wt_avionics  += bus.avionics.mass_properties.mass      
    
            for battery in bus.batteries: 
                W_energy_network_total  += battery.mass_properties.mass * Units.kg
                  
            for propulsor in bus.propulsors:
                if 'motor' in propulsor: 
                    motor_mass = propulsor.motor.mass_properties.mass                            
                    W_energy_network.motors += motor_mass 
                    W_energy_network_total  += motor_mass
                  
    network.mass_properties.mass = W_energy_network_total
    
    ##-------------------------------------------------------------------------------                 
    # Pod Weight Weight 
    ##-------------------------------------------------------------------------------         
    WPOD  = 0.0             
    if method_type == 'FLOPS Complex': 
        NENG   = network_number_of_engines
        WTNFA  = W_energy_network.wt_eng + W_energy_network.wt_thrust_reverser + W_energy_network.wt_starter \
                + 0.25 * W_energy_network.wt_engine_controls + 0.11 * wt_sys.wt_instruments + 0.13 * wt_sys.wt_elec \
                + 0.13 * wt_sys.wt_hyd_pnu + 0.25 * W_energy_network.fuel_system
        WPOD += WTNFA / np.max([1, NENG]) + W_energy_network.nacelle / np.max(
            [1.0, NENG + 1. / 2 * (NENG - 2 * np.floor(NENG / 2.))])
 
    output.propulsion_breakdown.total               = W_energy_network_total
    output.propulsion_breakdown.battery             = W_energy_network.battery
    output.propulsion_breakdown.engines             = W_energy_network.wt_eng
    output.propulsion_breakdown.thrust_reversers    = W_energy_network.wt_thrust_reverser
    output.propulsion_breakdown.miscellaneous       = W_energy_network.wt_engine_controls + W_energy_network.wt_starter
    output.propulsion_breakdown.fuel_system         = W_energy_network.fuel_system 

    ##-------------------------------------------------------------------------------                 
    # Wing Weight 
    ##------------------------------------------------------------------------------- 
    Al_rho   = Aluminum().density
    Al_sigma = Aluminum().yield_tensile_strength      
    
    num_main_wings      = 0
    wt_main_wing        = 0.0
    wt_tail_horizontal  = 0.0
    wt_tail_vertical    = 0.0
    for wing in vehicle.wings:
        if isinstance(wing, Wings.Main_Wing):
            num_main_wings += 1
    
    for wing in vehicle.wings:
        if isinstance(wing, Wings.Main_Wing): 
            if method_type == 'RCAIDE':
                wt_wing = Common.compute_main_wing_weight(vehicle, wing, Al_rho, Al_sigma)
            elif method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
                complexity = method_type.split()[1]
                wt_wing = FLOPS.compute_wing_weight(vehicle, wing, WPOD, complexity, settings, num_main_wings)
            elif method_type == 'Raymer':
                wt_wing = Raymer.compute_main_wing_weight(vehicle, wing)
            else:
                raise ValueError("This weight method is not yet implemented")
            # Apply weight factor
            wt_wing = wt_wing * (1. - wt_factors.main_wing) * (1. - wt_factors.structural)
            if np.isnan(wt_wing):
                wt_wing = 0.
            wing.mass_properties.mass = wt_wing
            wt_main_wing += wt_wing
        if isinstance(wing, Wings.Horizontal_Tail):
            if method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
                wt_tail = FLOPS.compute_horizontal_tail_weight(vehicle, wing)
            elif method_type == 'Raymer':
                wt_tail = Raymer.compute_horizontal_tail_weight(vehicle, wing)
            else:
                wt_tail = Transport.compute_horizontal_tail_weight(vehicle, wing)
            if type(wt_tail) == np.ndarray:
                wt_tail = sum(wt_tail)
            # Apply weight factor
            wt_tail = wt_tail * (1. - wt_factors.empennage) * (1. - wt_factors.structural)
            # Pack and sum
            wing.mass_properties.mass = wt_tail
            wt_tail_horizontal += wt_tail
        if isinstance(wing, Wings.Vertical_Tail):
            if method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
                wt_tail = FLOPS.compute_vertical_tail_weight(vehicle, wing)
            elif method_type == 'Raymer':
                wt_tail = Raymer.compute_vertical_tail_weight(vehicle, wing)
            else:
                wt_tail = Transport.compute_vertical_tail_weight(vehicle, wing)
            # Apply weight factor
            wt_tail = wt_tail * (1. - wt_factors.empennage) * (1. - wt_factors.structural)
            # Pack and sum
            wing.mass_properties.mass = wt_tail
            wt_tail_vertical += wt_tail
        
    ##-------------------------------------------------------------------------------                 
    # Fuselage 
    ##------------------------------------------------------------------------------- 
    wt_fuse_total = 0
    for fuse in vehicle.fuselages:
        if method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
            wt_fuse = FLOPS.compute_fuselage_weight(vehicle)
        elif method_type == 'Raymer':
            wt_fuse = Raymer.compute_fuselage_weight(vehicle, fuse, settings)
        else:
            wt_fuse = Transport.compute_fuselage_weight(vehicle, fuse, wt_main_wing, W_energy_network_total)
        wt_fuse = wt_fuse * (1. - wt_factors.fuselage) * (1. - wt_factors.structural)
        fuse.mass_properties.mass = wt_fuse
        wt_fuse_total += wt_fuse
    
    ##-------------------------------------------------------------------------------                 
    # Landing Gear Weight
    ##------------------------------------------------------------------------------- 
    if method_type == 'FLOPS Simple' or method_type == 'FLOPS Complex':
        landing_gear = FLOPS.compute_landing_gear_weight(vehicle)
    elif method_type == 'Raymer':
        landing_gear = Raymer.compute_landing_gear_weight(vehicle)
    else:
        landing_gear =  Common.compute_landing_gear_weight(vehicle)

    
    ##-------------------------------------------------------------------------------                 
    # Accumulate Structural Weight
    ##-------------------------------------------------------------------------------  
    output                                  = Data()
    output.structures                       = Data()
    output.structures.wing                  = wt_main_wing
    output.structures.horizontal_tail       = wt_tail_horizontal
    output.structures.vertical_tail         = wt_tail_vertical
    output.structures.fuselage              = wt_fuse_total
    output.structures.main_landing_gear     = landing_gear.main
    output.structures.nose_landing_gear     = landing_gear.nose 
    output.structures.nacelle               = W_energy_network.nacelle
    if 'FLOPS' in method_type:
        print('Paint weight is currently ignored in FLOPS calculations.')
    output.structures.paint = 0  # TODO reconcile FLOPS paint calculations with Raymer and RCAIDE baseline
    output.structures.total = output.structures.wing + output.structures.horizontal_tail + output.structures.vertical_tail \
                              + output.structures.fuselage + output.structures.main_landing_gear + output.structures.nose_landing_gear \
                              + output.structures.paint + output.structures.nacelle 

    ##-------------------------------------------------------------------------------                 
    # Accumulate Systems Weight
    ##-------------------------------------------------------------------------------     
    output.systems_breakdown                        = Data()
    output.systems_breakdown.control_systems        = wt_sys.wt_flight_control
    output.systems_breakdown.apu                    = wt_sys.wt_apu
    output.systems_breakdown.electrical             = wt_sys.wt_elec
    output.systems_breakdown.avionics               = wt_sys.wt_avionics
    output.systems_breakdown.hydraulics             = wt_sys.wt_hyd_pnu
    output.systems_breakdown.furnish                = wt_sys.wt_furnish
    output.systems_breakdown.air_conditioner        = wt_sys.wt_ac + wt_sys.wt_anti_ice # Anti-ice is sometimes included in ECS
    output.systems_breakdown.instruments            = wt_sys.wt_instruments
    output.systems_breakdown.total                  = output.systems_breakdown.control_systems + output.systems_breakdown.apu \
                                                    + output.systems_breakdown.electrical + output.systems_breakdown.avionics \
                                                    + output.systems_breakdown.hydraulics + output.systems_breakdown.furnish \
                                                    + output.systems_breakdown.air_conditioner + output.systems_breakdown.instruments

    output.payload_breakdown    = Data()
    output.payload_breakdown    = payload 
    output.operational_items    = Data()
    output.operational_items    = wt_oper 
    output.empty                = output.structures.total + output.propulsion_breakdown.total + output.systems_breakdown.total
    output.operating_empty      = output.empty + output.operational_items.total
    output.zero_fuel_weight     = output.operating_empty + output.payload_breakdown.total
    output.max_takeoff          = vehicle.mass_properties.max_takeoff
    fuel_mass                   = vehicle.mass_properties.max_takeoff - output.zero_fuel_weight 

    #for network in vehicle.networks:  
        #for fuel_line in  network.fuel_lines: 
            #for fuel_tank in fuel_line.fuel_tanks:
                #pass
                    
    if not hasattr(vehicle.landing_gear, 'nose'):
        vehicle.landing_gear.nose   =  RCAIDE.Library.Components.Landing_Gear.Nose_Landing_Gear()
    vehicle.landing_gear.nose.mass  = output.structures.nose_landing_gear
    if not hasattr(vehicle.landing_gear, 'main'):
        vehicle.landing_gear.main   =  RCAIDE.Library.Components.Landing_Gear.Main_Landing_Gear()   
    vehicle.landing_gear.main.mass  = output.structures.main_landing_gear  

    control_systems                         = RCAIDE.Library.Components.Component()
    control_systems.mass_properties.mass    = output.systems_breakdown.control_systems
    electrical_systems                      = RCAIDE.Library.Components.Component()
    electrical_systems.mass_properties.mass = output.systems_breakdown.electrical
    furnishings                             = RCAIDE.Library.Components.Component()
    furnishings.mass_properties.mass        = output.systems_breakdown.furnish
    avionics                                = RCAIDE.Library.Components.Systems.Avionics()
    avionics.mass_properties.mass           = output.systems_breakdown.avionics + output.systems_breakdown.instruments
    air_conditioner                         = RCAIDE.Library.Components.Component() 
    air_conditioner.mass_properties.mass    = output.systems_breakdown.air_conditioner
    apu                                     = RCAIDE.Library.Components.Component()
    apu.mass_properties.mass                = output.systems_breakdown.apu
    hydraulics                              = RCAIDE.Library.Components.Component()
    hydraulics.mass_properties.mass         = output.systems_breakdown.hydraulics
    optionals                               = RCAIDE.Library.Components.Component()
    optionals.mass_properties.mass          = output.operational_items.operating_items_less_crew
    
    # assign components to vehicle
    vehicle.systems.control_systems         = control_systems
    vehicle.systems.electrical_systems      = electrical_systems
    vehicle.systems.avionics                = avionics
    vehicle.systems.furnishings             = furnishings
    vehicle.systems.air_conditioner         = air_conditioner 
    vehicle.systems.apu                     = apu
    vehicle.systems.hydraulics              = hydraulics
    vehicle.systems.optionals               = optionals   

    return output
