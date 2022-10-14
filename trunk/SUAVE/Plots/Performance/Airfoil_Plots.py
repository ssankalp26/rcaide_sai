## @ingroup Plots
# Airfoil_Plots.py
#
# Created:  Mar 2021, M. Clarke
# Modified: Feb 2022, M. Clarke
# Modified: Sep 2022, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import SUAVE
from SUAVE.Core import Units
from SUAVE.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil.import_airfoil_polars \
     import import_airfoil_polars 
from SUAVE.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil.compute_airfoil_properties \
     import compute_airfoil_properties
from SUAVE.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil.import_airfoil_geometry \
     import import_airfoil_geometry
import numpy as np 
import matplotlib.pyplot as plt  
import matplotlib.cm as cm
import os
 
## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method
def plot_airfoil_analysis_boundary_layer_properties(ap,show_legend = False ):
    """Plots viscous distributions
    
    Assumptions:
    None
    
    Source: 
    None
                                                     
    Inputs:
        ap     : data stucture of airfoil boundary layer properties  
                                                                           
    Outputs:
        Figures of quantity distributions
    
    Properties Used:
    N/A
    """            
    
    plot_quantity(ap, ap.Ue_Vinf, r'$U_{e}/U_{inv}}$'  ,'inviscid edge velocity',show_legend) 
    plot_quantity(ap, ap.H,  r'$H$'  ,'kinematic shape parameter',show_legend)
    plot_quantity(ap, ap.delta_star, r'$\delta*$' ,'displacement thickness',show_legend)
    plot_quantity(ap, ap.delta   , r'$\delta$' ,'boundary layer thickness',show_legend)
    plot_quantity(ap, ap.theta, r'$\theta$' ,'momentum thickness',show_legend)
    plot_quantity(ap, ap.cf, r'$c_f $'  ,   'skin friction coefficient',show_legend)
    plot_quantity(ap, ap.Re_theta,  r'$Re_{\theta}$'  ,'theta Reynolds number',show_legend) 
    

    fig      = plt.figure()
    axis     = fig.add_subplot(1,1,1)       
    n_cpts   = len(ap.AoA[:,0])
    n_cases  = len(ap.AoA[0,:]) 

    # create array of colors for difference reynolds numbers     
    blues  = cm.winter(np.linspace(0, 0.75,n_cases))    
    reds   = cm.autumn(np.linspace(0, 0.75,n_cases)) 
    
    for i in range(n_cpts):   
        for j in range(n_cases): 
            case_label = 'AoA: ' + str(round(ap.AoA[i,j]/Units.degrees, 2)) + ', Re: ' + str(ap.Re[i,j]) 
            axis.plot(ap.x[i,j], ap.y[i,j], color = blues[j] , linewidth = 2, label = case_label ) 
            axis.plot(ap.x_bl[i,j], ap.y_bl[i,j], color = reds[j] , marker = 'o', linewidth = 2, label = case_label ) 
            
    axis.set_title('Airfoil with Boundary Layers')            
    axis.set_ylabel(r'$y$') 
    axis.set_xlabel(r'$x$') 
    if show_legend:
        axis.legend(loc='upper left', ncol=1)    
    
    
    return    
 

## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method
def plot_quantity(ap, q, qaxis, qname,show_legend):
    """Plots a quantity q over lower/upper/wake surfaces
    
    Assumptions:
    None
    
    Source: 
    None
                                                     
    Inputs:
       ap        : data stucture of airfoil boundary layer properties  
       q         : vector of values to plot, on all points (wake too if present)
       qaxis     : name of quantity, for axis labeling
       qname     : name of quantity, for title labeling
                                                                           
    Outputs:
       Figure showing q versus x
    
    Properties Used:
    N/A
    """          

    fig      = plt.figure()
    axis     = fig.add_subplot(1,1,1)       
    n_cpts   = len(ap.AoA[:,0])
    n_cases  = len(ap.AoA[0,:]) 

    # create array of colors for difference reynolds numbers     
    blues  = cm.winter(np.linspace(0, 0.75,n_cases)) 
    
    for i in range(n_cpts):   
        for j in range(n_cases): 
            case_label = 'AoA: ' + str(round(ap.AoA[i,j]/Units.degrees, 2)) + ', Re: ' + str(ap.Re[i,j]) 
            axis.plot(ap.x[i,j], q[i,j], color = blues[j] , marker = 'o', linewidth = 2, label = case_label ) 
            
    axis.set_title(qname)            
    axis.set_ylabel(qaxis) 
    axis.set_xlabel(r'$x$') 
    if show_legend:
        axis.legend(loc='upper left', ncol=1)
    return  
 
## @ingroup Plots
def plot_airfoil_analysis_surface_forces(ap,show_legend= True,arrow_color = 'r'):  
    """ This plots the forces on an airfoil surface
    
        Assumptions:
        None
        
        Inputs: 
        ap       - data stucture of airfoil boundary layer properties and polars 
         
        Outputs: 
        None 
        
        Properties Used:
        N/A
        """        
    
    # determine dimension of angle of attack and reynolds number 
    n_cpts   = len(ap.AoA[:,0])
    n_cases  = len(ap.AoA[0,:])
    n_pts    = len(ap.x[0,0,:])-1
    

    for i in range(n_cpts):     
        for j in range(n_cases): 
            label =  '_AoA_' + str(round(ap.AoA[i,j]/Units.degrees,2)) + '_deg_Re_' + str(round(ap.Re[i,j]/1000000,2)) + 'E6'
            fig   = plt.figure('Airfoil_Pressure_Normals' + label )
            axis = fig.add_subplot(1,1,1) 
            axis.plot(ap.x[0,0,:], ap.y[0,0,:],'k-')   
            for k in range(n_pts):
                dx_val = ap.normals[i,j,k,0]*abs(ap.cp[i,j,k])*0.1
                dy_val = ap.normals[i,j,k,1]*abs(ap.cp[i,j,k])*0.1
                if ap.cp[i,j,k] < 0:
                    plt.arrow(x= ap.x[i,j,k], y=ap.y[i,j,k] , dx= dx_val , dy = dy_val , 
                              fc=arrow_color, ec=arrow_color,head_width=0.005, head_length=0.01 )   
                else:
                    plt.arrow(x= ap.x[i,j,k]+dx_val , y= ap.y[i,j,k]+dy_val , dx= -dx_val , dy = -dy_val , 
                              fc=arrow_color, ec=arrow_color,head_width=0.005, head_length=0.01 )   
    
    return   



def plot_airfoil_polar_files(airfoil_path, airfoil_polar_paths, line_color = 'k-', use_surrogate = False,
                             save_figure = False, save_filename = "Airfoil_Polars", file_type = ".png"):
    """This plots all airfoil polars in the list "airfoil_polar_paths" 

    Assumptions:
    None

    Source:
    None

    Inputs:
    airfoil_polar_paths   [list of strings]

    Outputs: 
    Plots

    Properties Used:
    N/A	
    """
    shape = np.shape(airfoil_polar_paths)
    n_airfoils = shape[0]
    n_Re       = shape[1]
    
    if use_surrogate:
        # Compute airfoil surrogates
        airfoil_geometry = import_airfoil_geometry(airfoil_path)
        a_data           = compute_airfoil_properties(airfoil_geometry, airfoil_polar_paths, use_pre_stall_data=False)
        CL_sur           = a_data.lift_coefficient_surrogates
        CD_sur           = a_data.drag_coefficient_surrogates
                
        alpha            = np.asarray(a_data.aoa_from_polar) * Units.degrees
        n_alpha          = len(alpha.T)
        alpha            = np.reshape(alpha,(n_airfoils,1,n_alpha))
        alpha            = np.repeat(alpha, n_Re, axis=1)
                 
        Re               = a_data.re_from_polar
        Re               = np.reshape(Re,(n_airfoils,n_Re,1))
        Re               = np.repeat(Re, n_alpha, axis=2)

        CL = np.zeros_like(Re)
        CD = np.zeros_like(Re)

    else:
        # Use the raw data polars
        airfoil_polar_data = import_airfoil_polars(airfoil_polar_paths)
        CL = airfoil_polar_data.lift_coefficients
        CD = airfoil_polar_data.drag_coefficients
        
        n_alpha = np.shape(CL)[2]
        Re = airfoil_polar_data.reynolds_number
        Re = np.reshape(Re, (n_airfoils,n_Re,1))
        Re = np.repeat(Re, n_alpha, axis=2)


    for i in range(n_airfoils):
        airfoil_name = os.path.basename(airfoil_path[i][0])
        if use_surrogate:
            CL[i,:,:] = CL_sur[airfoil_path[i]]((Re[i,:,:],alpha[i,:,:]))
            CD[i,:,:] = CD_sur[airfoil_path[i]]((Re[i,:,:],alpha[i,:,:]))
            
        # plot all Reynolds number polars for ith airfoil
        fig  = plt.figure(save_filename +'_'+ str(i))
        fig.set_size_inches(10, 4)
        axes = fig.add_subplot(1,1,1)
        axes.set_title(airfoil_name)            
        for j in range(n_Re):
            Re_val = str(round(Re[i,j,0]))
            axes.plot(CD[i,j,:], CL[i,j,:], label='Re='+Re_val)
            
        axes.set_xlabel('$C_D$')  
        axes.set_ylabel('$C_L$')  
        axes.legend(bbox_to_anchor=(1,1), loc='upper left', ncol=1)
        
        if save_figure:
            plt.savefig(save_filename +'_' + str(i) + file_type)    
    return


def plot_airfoil_aerodynamic_coefficients(airfoil_path, airfoil_polar_paths, line_color = 'k-', use_surrogate = True,
                                          save_figure = False, save_filename = "Airfoil_Polars", file_type = ".png"):
    """This plots all airfoil polars in the list "airfoil_polar_paths" 

    Assumptions:
    None

    Source:
    None

    Inputs:
    airfoil_polar_paths   [list of strings]

    Outputs: 
    Plots

    Properties Used:
    N/A	
    """
    shape = np.shape(airfoil_polar_paths)
    n_airfoils = shape[0]
    n_Re       = shape[1]

    col_raw = ['m-', 'b-', 'r-', 'g-', 'k-','m-','b-','r-','g-', 'k-']    
    if use_surrogate:
        col_sur = ['m--', 'b--', 'r--', 'g--', 'k--','m--','b--','r--', 'g--', 'k--']
        # Compute airfoil surrogates
        a_data = compute_airfoil_properties(airfoil_path, airfoil_polar_paths,npoints = 200, use_pre_stall_data=True)
        CL_sur = a_data.lift_coefficient_surrogates
        CD_sur = a_data.drag_coefficient_surrogates
        
        alpha   = np.asarray(a_data.aoa_from_polar) * Units.deg
        n_alpha = len(alpha.T)
        alpha   = np.reshape(alpha,(n_airfoils,1,n_alpha))
        alpha   = np.repeat(alpha, n_Re, axis=1)
        
        Re      = a_data.re_from_polar
        Re      = np.reshape(Re,(n_airfoils,n_Re,1))
        Re      = np.repeat(Re, n_alpha, axis=2)

        CL = np.zeros_like(Re)
        CD = np.zeros_like(Re)
    
        for i in range(n_airfoils):
            CL[i,:,:] = CL_sur[airfoil_path[i]]((Re[i,:,:],alpha[i,:,:]))
            CD[i,:,:] = CD_sur[airfoil_path[i]]((Re[i,:,:],alpha[i,:,:]))      
    
    # Get raw data polars
    airfoil_polar_data = import_airfoil_polars(airfoil_polar_paths)
    CL_raw      = airfoil_polar_data.lift_coefficients
    CD_raw      = airfoil_polar_data.drag_coefficients
    alpha_raw   = airfoil_polar_data.angle_of_attacks
    n_alpha_raw = len(alpha_raw)        
    
    # reshape into Re and n_airfoils
    alpha_raw  = np.tile(alpha_raw, (n_airfoils,n_Re,1))
    
    Re = airfoil_polar_data.reynolds_number
    Re = np.reshape(Re, (n_airfoils,n_Re,1))
    Re = np.repeat(Re, n_alpha_raw, axis=2)
    
    for i in range(n_airfoils):
        airfoil_name = os.path.basename(airfoil_path[i])
            
        # plot all Reynolds number polars for ith airfoil
        fig  = plt.figure(airfoil_name[:-4], figsize=(8,2*n_Re))
          
        for j in range(n_Re):
            ax1    = fig.add_subplot(n_Re,2,1+2*j)
            ax2    = fig.add_subplot(n_Re,2,2+2*j)  
            
            Re_val = str(round(Re[i,j,0])/1e6)+'e6'
            ax1.plot(alpha_raw[i,j,:], CL_raw[i,j,:], col_raw[j], label='Re='+Re_val)
            ax2.plot(alpha_raw[i,j,:], CD_raw[i,j,:], col_raw[j], label='Re='+Re_val)
            if use_surrogate:
                ax1.plot(alpha[i,j,:]/Units.deg, CL[i,j,:], col_sur[j])
                ax2.plot(alpha[i,j,:]/Units.deg, CD[i,j,:], col_sur[j])
             
            ax1.set_ylabel('$C_l$')   
            ax2.set_ylabel('$C_d$')  
            ax1.legend(loc='best')
            
        ax1.set_xlabel('AoA [deg]') 
        ax2.set_xlabel('AoA [deg]') 
        fig.tight_layout()
        
        if save_figure:
            plt.savefig(save_filename +'_' + str(i) + file_type)
    return