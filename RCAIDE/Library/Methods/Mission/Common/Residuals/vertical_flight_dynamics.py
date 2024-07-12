## @ingroup Library-Methods-Missions-Common-Residuals
# RCAIDE/Library/Methods/Missions/Common/Residuals/vertical_flight_dynamics.py
# 
# 
# Created:  Jul 2023, M. Clarke
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import RCAIDE
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Missions-Common-Residuals  
def vertical_flight_dynamics(segment):
    """ Calculates a residual based on forces
    
        Assumptions:
        The vehicle is not accelerating, doesn't use gravity. Only vertical forces
        
        Inputs:
            state.conditions:
                frames.inertial.total_force_vector [Newtons]
            
        Outputs:
            state.residuals.forces [meters/second^2]

        Properties Used:
        N/A
                                
    """      
    if 'acceleration' in segment:
        ax      = segment.acceleration  
        one_row = segment.state.ones_row 
        a       = one_row(3)*0
        a[:,0]  = ax 
        segment.state.conditions.frames.inertial.acceleration_vector = a 
        
    FT      = segment.state.conditions.frames.inertial.total_force_vector
    a       = segment.state.conditions.frames.inertial.acceleration_vector    
    MT      = segment.state.conditions.frames.inertial.total_moment_vector    
    ang_acc = segment.state.conditions.frames.inertial.angular_acceleration_vector  
    m       = segment.state.conditions.weights.total_mass
    I       = segment.analyses.aerodynamics.geometry.mass_properties.moments_of_inertia.tensor 
    
    if segment.flight_dynamics.force_x: 
        segment.state.residuals.force_x[:,0] = FT[:,0]/m[:,0] - a[:,0]
    if segment.flight_dynamics.force_y: 
        segment.state.residuals.force_y[:,0] = FT[:,1]/m[:,0] - a[:,1]       
    if segment.flight_dynamics.force_z: 
        segment.state.residuals.force_z[:,0] = FT[:,2]/m[:,0] - a[:,2]  
    if  segment.flight_dynamics.moment_x:
        segment.state.residuals.moment_x[:,0] = MT[:,0]/I[0,0] - ang_acc[:,0]   
    if  segment.flight_dynamics.moment_y:
        segment.state.residuals.moment_y[:,0] = MT[:,1]/I[1,1] - ang_acc[:,1]   
    if  segment.flight_dynamics.moment_z:
        segment.state.residuals.moment_z[:,0] = MT[:,2]/I[2,2] - ang_acc[:,2]     

    return
    
    
 
    
