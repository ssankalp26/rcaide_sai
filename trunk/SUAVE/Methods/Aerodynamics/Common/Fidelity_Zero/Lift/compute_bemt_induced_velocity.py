## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Lift
# compute_bemt_induced_velocity.py
# 
# Created:  Jun 2021, R. Erhard 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# package imports
import numpy as np 
from scipy.interpolate import interp1d

## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Lift 
def compute_bemt_induced_velocity(prop,geometry):  
    """ This computes the velocity induced by the BEMT wake
    on lifting surface control points

    Assumptions:  
       The wake contracts following formulation by McCormick.
    
    Source:   
       Contraction factor: McCormick 1969, Aerodynamics of V/STOL Flight
       
    Inputs: 
       prop        - propeller or rotor data structure             [Unitless] 
       geometry    - SUAVE vehicle                                 [Unitless] 

    Properties Used:
       N/A
    """    
    # extract parameters
    VD = geometry.vortex_distribution
    R  = prop.tip_radius
    
    # contraction factor by McCormick
    s  = geometry.wings.main_wing.origin[0][0] - prop.origin[0][0]
    kd = 1 + s/(np.sqrt(s**2 + R**2))

    # extract radial and azimuthal velocities at blade
    va = kd*prop.outputs.blade_axial_induced_velocity[0]
    vt = kd*prop.outputs.blade_tangential_induced_velocity[0]
    r  = prop.outputs.disc_radial_distribution[0][0]
    
    hub_y_center = prop.origin[0][1]
    prop_y_min   = hub_y_center - r[-1]
    prop_y_max   = hub_y_center + r[-1]
    
    prop_V_wake_ind = np.zeros((1,VD.n_cp,3)) # one mission control point, n_cp wing control points, 3 velocity components
    
    ir = prop_y_min+r
    ro = np.flipud(prop_y_max-r)
    prop_y_range = np.append(ir, ro)
    

    # within this range, add an induced x- and z- velocity from propeller wake
    bool_in_range = (abs(VD.YC)>ir[0])*(abs(VD.YC)<ro[-1])
    YC_in_range   = VD.YC[bool_in_range]
    
    va_y_range  = np.append(np.flipud(va), va)
    vt_y_range  = np.append(np.flipud(vt), vt)*prop.rotation[0]
    va_interp   = interp1d(prop_y_range, va_y_range)
    vt_interp   = interp1d(prop_y_range, vt_y_range)
    
    y_vals  = YC_in_range
    val_ids = np.where(bool_in_range==True)
    
    # check if y values are inboard of propeller axis
    inboard_bools = abs(y_vals)<hub_y_center
    
    # preallocate va_new and vt_new
    va_new = np.zeros(np.size(val_ids))
    vt_new = np.zeros(np.size(val_ids))
    
    # take absolute y values (symmetry)
    va_new = va_interp(abs(y_vals))
    
    # inboard vt values
    vt_new[inboard_bools]        = -vt_interp(abs(y_vals[inboard_bools]))
    vt_new[inboard_bools==False] = vt_interp(abs(y_vals[inboard_bools==False]))
    
    prop_V_wake_ind[0,val_ids,0] = va_new  # axial induced velocity
    prop_V_wake_ind[0,val_ids,1] = 0       # spanwise induced velocity; in line with prop, so 0
    prop_V_wake_ind[0,val_ids,2] = vt_new  # vertical induced velocity      
    
       
    return prop_V_wake_ind
  
  