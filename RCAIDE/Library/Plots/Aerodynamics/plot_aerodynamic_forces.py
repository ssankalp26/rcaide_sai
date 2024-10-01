## @ingroup Library-Plots-Performance-Aerodynamics
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_aerodynamic_forces.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Plots-Performance-Aerodynamics
def plot_aerodynamic_forces(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Aerodynamic_Forces",
                             file_type = ".png",
                             width = 8, height = 6):
    """This plots the aerodynamic forces
    
    Assumptions:
    None
    
    Source:
    None
    
    Inputs:
    results.segments.condtions.frames
         body.thrust_force_vector
         wind.force_vector
         wind.force_vector
         
    Outputs:
    Plots
    
    Properties Used:
    N/A
    """ 

    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))     
    
    fig1   = plt.figure(save_filename+'_Power')
    fig1.set_size_inches(width,height)
    fig2   = plt.figure(save_filename+'_Thrust')
    fig2.set_size_inches(width,height)
    fig3   = plt.figure(save_filename+'_Lift')
    fig3.set_size_inches(width,height)
    fig4   = plt.figure(save_filename+'_Drag')
    fig4.set_size_inches(width,height)
    
    axis_1 = fig1.add_subplot(1, 1, 1)
    axis_2 = fig2.add_subplot(1, 1, 1)
    axis_3 = fig3.add_subplot(1, 1, 1)
    axis_4 = fig4.add_subplot(1, 1, 1)
    
    
    for i in range(len(results.segments)): 
        time   = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        Power  = results.segments[i].conditions.energy.power[:,0] 
        Thrust = results.segments[i].conditions.frames.body.thrust_force_vector[:,0]
        Lift   = -results.segments[i].conditions.frames.wind.force_vector[:,2]
        Drag   = -results.segments[i].conditions.frames.wind.force_vector[:,0]
        
                       
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
        
        # power
        axis_1.set_xlabel('Time (mins)')
        axis_1.set_ylabel(r'Power (MW)')
        axis_1.plot(time,Power/1E6, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size) 
        set_axes(axis_1)                
        
        axis_2.set_xlabel('Time (mins)')
        axis_2.set_ylabel(r'Thrust (kN)')
        axis_2.plot(time, Thrust/1000, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)         
        set_axes(axis_2) 

        axis_3.plot(time, Lift/1000, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'Lift (kN)')
        set_axes(axis_3) 
        
        axis_4.plot(time,Drag/1000 , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name,markersize = ps.marker_size)
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylabel(r'Drag (kN)')
        set_axes(axis_4)  
        
 
    if show_legend:    
        leg1 =  fig1.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg2 =  fig2.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg3 =  fig3.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5)
        leg4 =  fig4.legend(bbox_to_anchor=(0.5, 1.0), loc='upper center', ncol = 5) 
        leg1.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg2.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg3.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})
        leg4.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})   
    
    # Adjusting the sub-plots for legend 
    fig1.subplots_adjust(top=0.8)
    fig2.subplots_adjust(top=0.8)
    fig3.subplots_adjust(top=0.8)
    fig4.subplots_adjust(top=0.8)
    
    # set title of plot 
    
    if save_figure:
        fig1.savefig(save_filename + '_Power' + file_type)
        fig2.savefig(save_filename + '_Thrust' + file_type)
        fig3.savefig(save_filename + '_Lift' + file_type)
        fig4.savefig(save_filename + '_Drag' + file_type)  
    return fig1,fig2,fig3,fig4 
