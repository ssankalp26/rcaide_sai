
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Data 
from RCAIDE.Energy.Energy_Component            import Energy_Component
# package imports 
import numpy as np
from scipy.optimize import minimize

# ----------------------------------------------------------------------------------------------------------------------
# Conjugate_Heat_Removal_System  
# ----------------------------------------------------------------------------------------------------------------------
class Conjugate_Heat_Removal_System():
    
    def __defaults__(self):  
        self.tag                                      = 'Conjugate_Heat_Removal_System';  
        self.heat_transfer_efficiency                 = 1.0;
        
    
# ----------------------------------------------------------------------
#  Methods
# ----------------------------------------------------------------------

def design_conjugate_cooling_heat_removal_system(battery,Q_gen):
    
    # ---------------------------------------------------------------------
    #   Inital Channel Geometric Properties 
    # ---------------------------------------------------------------------     
    heat_gen=Data(
    b= 0.5,                         # Thickness of the Chanel through which condcution occurs (Replace with funciton)
    d= 0.5,                        # width of the channel (Replace with function)
    c= 0.3,                        # height of the channel (Replace with function)
    theta=47.5,                    # Contact Arc angle in degrees 
    
    #calculate the  surface area of the channel 
    A_chan=heat_gen.N_battery*heat_gen.theta*heat_gen.A_cell/360,
    # calculate hydraullic diameter   
    dh= (4*heat_gen.c*heat_gen.d)/(2*(heat_gen.c+heat_gen.d)),
    # calculate the aspect ratio
    ar= heat_gen.d/heat_gen.c,    
    
    # ---------------------------------------------------------------------
    #  Unpack Battery Properties  
    # ---------------------------------------------------------------------     
    
    d_cell=0.5,                    # Diameter of each cell (Replace with funciton)
    h_cell= 0.5,                   # Height of the cell (Replace with function)
    A_cell=np.pi*heat_gen.d_cell*heat_gen.h_cell,    # Area of Cell
    N_battery= 10,                 # Number of Batteries (Replace with funciton)
    T_Battrey=600,                 # Temperature of battery
    Q_gen= 1655,                    # Heat Generated by battery (Replace with funciton)
    # ---------------------------------------------------------------------
    #   Unpack Input Thermophysical Properties
    # --------------------------------------------------------------------- 
    # coolant liquid   
    rho=1022,                      # Density of the Coolant (Replace with function)
    mu= 0.0015,                    # Dynamic Viscosity of the Coolant (Replace with function)
    Pr=6.9,                        #Prandtl Number of Coolant (Replace with function)
    k_lq= 0.8,                     # Conductivity of the Coolant (Replace with function)
    cp=4.186,                      #Specific Heat of the Coolant (Replace with function)
    Ti=278,                        # Coolant temperature of the Coolant (A function of the outlet tempature of the HEX)
    
    # channel (solid attributes)
    k_chan=237                  # Conductivity of the Channel (Replace with function)
    )
          
    # set up optimization using scipy optimize 
  
    # solve for mass flow rate in the channel    
    opt_params = size_conjugate_cooling(Q_gen, battery,heat_gen)
        
    m_coolant =  opt_params[0]
    Q_convec=opt_params[1]-Q_gen    #add correct variable 
    
    return 


 
def size_conjugate_cooling(Q_gen, battery, heat_gen, m_coolant_lower_bound=0.01,  m_coolant_upper_bound=10.0): 

    
    # objective  
    
    args = (    )
    
    hard_cons = [ ] 
    
    bnds = (m_coolant_lower_bound, m_coolant_upper_bound);

    sol = minimize(objective, m_coolant=0.5, args=(m_coolant) , method='SLSQP', bounds=bnds, tol=1e-6, constraints=hard_cons) 
    
    return sol.x   


# objective function
def objective( heat_gen ) : 
    
    # m_coolant is the variable that needs to be optimized for a given channel
  
    # ---------------------------------------------------------------------
    #   Claculate Q_convec as a function of m_coolant
    # --------------------------------------------------------------------- 
    
    #calculate the velocity of the fluid in the channel 
    v=heat_gen.rho*heat_gen.c*heat_gen.d*m_coolant;
    
    # calculate the Reynolds Number 
    Re=(heat_gen.rho*heat_gen.dh*v)/heat_gen.mu;
    
    # fanning friction factor (eq 32)
    if Re< 2300:
        f= 24*(1-(1.3553*heat_gen.ar)+(1.9467*heat_gen.ar**2)-(1.7012*heat_gen.ar**3)+(0.9564*heat_gen.ar**4)-(0.2537*heat_gen.ar**5));
    elif Re>=2300:
        f= (0.0791*(Re**(-0.25)))*(1.8075-0.1125*heat_gen.ar);
        
    # Nusselt Number (eq 12)   
    if Re< 2300:
        Nu= 8.235*(1-(2.0421*heat_gen.ar)+(3.0853*heat_gen.ar**2)-(2.4765*heat_gen.ar**3)+(1.0578*heat_gen.ar**4)-(0.1861*heat_gen.ar**5));    
    elif Re >= 2300:
        Nu = ((f/2)*(Re-1000)*heat_gen.Pr)/(1+(12.7*(f**0.5)*(heat_gen.Pr**(2/3)-1)));   
    
    # heat transfer coefficient of the channeled coolant (eq 11)
    h= heat_gen.k_lq*Nu/heat_gen.dh;
    
    # Overall Heat Transfer Coefficient from battery surface to the coolant fluid (eq 10)
    U_total = 1/((1/h)+(heat_gen.b/heat_gen.k_chan));
    
    # Calculate NTU
    NTU= U_total*heat_gen.A_chan/(m_coolant*heat_gen.cp);
    
    # Calculate Outlet Temparture To ( eq 8)
    To=((heat_gen.T_Battrey-heat_gen.Ti)*(1-np.exp(-NTU)))+heat_gen.Ti;
    
    # Calculate the Log mean temperature 
    T_lm = ((heat_gen.T_Battrey-heat_gen.Ti)-(heat_gen.T_Battrey-To))/(np.log((heat_gen.T_Battrey-heat_gen.Ti)/(heat_gen.T_Battrey-To)));
    
    # Calculated Heat Convected 
    Q_conv=U_total*heat_gen.A_chan*T_lm;
    
    #Residual 
    Res = heat_gen.Q_gen-Q_conv;
    
    return  Res 


# hard constraint
def constraint( ): 
    
    
    return  

 