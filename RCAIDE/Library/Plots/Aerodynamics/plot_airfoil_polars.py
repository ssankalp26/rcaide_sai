## @ingroup Library-Plots-Performance-Aerodynamics
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_airfoil_polars.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------     

## @ingroup Library-Plots-Performance-Aerodynamics   
def plot_airfoil_polars(polar_data,
                        save_figure   = False,
                        save_filename = "Airfoil_Polars",
                        file_type = ".png",
                        width = 8, height = 6):
    """This plots all the airfoil polars of a specfic airfoil

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
 
    # Get raw data polars 
    CL           = polar_data.cl_invisc[0]
    CD           = polar_data.cd_invisc[0]
    CM           = polar_data.cm_invisc[0]
    alpha        = polar_data.AoA[0]/Units.degrees
    Re_raw       = polar_data.Re[0]  
       
    Re_val = str(round(Re_raw[0])/1e6)+'e6' 
    
    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)
      
    fig1   = plt.figure(save_filename + "_Cl")
    fig2   = plt.figure(save_filename + "_Cd")
    fig3   = plt.figure(save_filename + "_Cm")
    fig4   = plt.figure(save_filename + "_Cl/Cd")
    
    fig1.set_size_inches(width,height)
    fig2.set_size_inches(width,height)
    fig3.set_size_inches(width,height)
    fig4.set_size_inches(width,height) 
               
    axis_1 = plt.subplot(1,1,1)
    axis_2 = plt.subplot(1,1,1)    
    axis_3 = plt.subplot(1,1,1)
    axis_4 = plt.subplot(1,1,1)
    
    axis_1.plot(alpha, CL, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width, label = 'Re = '+Re_val, markersize = ps.marker_size)
    axis_1.set_xlabel('AoA [deg]')
    axis_1.set_ylabel(r'$C_l$')
    set_axes(axis_1)    
  
    axis_2.plot(alpha, CD, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width, label = 'Re = '+Re_val, markersize = ps.marker_size)
    axis_2.set_xlabel('AoA [deg]')
    axis_2.set_ylabel(r'$C_d$')
    set_axes(axis_2) 

    axis_3.plot(alpha, CM, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width, label = 'Re = '+Re_val, markersize = ps.marker_size)
    axis_3.set_xlabel('AoA [deg]') 
    axis_3.set_ylabel(r'$C_m$')
    set_axes(axis_3) 
    
    axis_4.plot(alpha, CL/CD, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width, label = 'Re = '+Re_val, markersize = ps.marker_size)
    axis_4.set_xlabel('AoA [deg]')
    axis_4.set_ylabel(r'Cl/Cd')
    axis_4.set_ylim([-20,20])
    set_axes(axis_4) 
            
    if save_figure:
        fig1.savefig(save_filename + "_Cl" + file_type)
        fig2.savefig(save_filename + "_Cd" + file_type)
        fig3.savefig(save_filename + "_Cm" + file_type)
        fig4.savefig(save_filename + "_Cl/Cd" + file_type)  
    return  fig1, fig2, fig3, fig4
     
     
     
     