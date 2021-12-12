# initial parameters for PID controller

def initial_parameters_setting():
    initiag_args = {
        
      #proportional constant
    "kp" : 8,
    #integration constan
    "ki" : 0.1 ,
    #derivative constant
    "kd" : 2,   
    #initial control value
    "MV_initial": 0    
        
        
        
        
    }
    return initiag_args
   
    
