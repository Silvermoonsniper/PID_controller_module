%matplotlib inline
from tclab import clock, setup, Historian, Plotter
class PID_controller():
    
    #initial arguments setting
    def __init__(self,initial_args):
        for key in initial_args:
            setattr(self, key, initial_args[key])
    #initialize desired control value
        self.desired_value=40

#implement a Proportional controller 
# set up for proportional control portion
# INPUT ARGs:
#    kp: proportional constant
#    desired_value: desired control value
    def proportion_control(self,kp,desired_value):
    # set starting value of control
        MV=0
        
        while True:
        #update and return current measurement
            current_measurement= yield MV
            
            MV=kp*(desired_value-current_measurement)

            
# implement a PID controller
# input args:
#       kp: proportional constant
#       ki: integration constant
#       kd: derivative constant
#       MV_initial: initial control value
    def PID_control(self,kp,ki,kd,MV_initial):
        # initialize  error
        e_prev = 0
        # initial time
        t_prev = -100
        #st first, integration of error is zero
        I = 0
    
    # initial control
        MV = MV_initial
    
        while True:
        # yield MV, wait for new t, PV, SP
            t,current_measurement , desired_value = yield MV
        
        # PID calculations
            e = desired_value - current_measurement
        
            P = kp*e
            I = I + ki*e*(t - t_prev)
            D = kd*(e - e_prev)/(t - t_prev)
        
            MV = MV_initial + P + I + D
        
        # update stored data for next iteration
            e_prev = e
            t_prev = t
            
 #function to simulate a PID control experiment
    def PID_simulation(self,kp,ki,kd,MV_initial):
        TCLab = setup(connected=False, speedup=10)
        
        controller_FINAL = self.PID_control(kp,ki,kd,MV_initial)        # create pid control
        controller_FINAL.send(None)              # initialize

        tfinal = 800

        with TCLab() as lab:
            h = Historian([('SP', lambda: desired_value), ('T1', lambda: lab.T1), ('MV', lambda: MV), ('Q1', lab.Q1)])
            p = Plotter(h, tfinal)
            T1 = lab.T1
            for t in clock(tfinal, 2):
                desired_value = T1 if t < 50 else 50           # get setpoint
               
                current_measurement = lab.T1                         # get measurement
                MV = controller_FINAL.send([t, current_measurement, desired_value])   # compute manipulated variable
                lab.U1 = MV                         # apply 
                p.update(t)                         # update information display








#main program entrance
if __name__ == '__main__':
        #parameters setting
        initial_args = initial_parameters_setting()
        #call the class for PID controller
        controller = PID_controller(initial_args)
        
      #####################################################################################  
        #call Proportional controller with certain setpoint
      #  a=controller.proportion_control(controller.kp,controller.desired_value)
        a = controller.proportion_control(40,10)
      # start the generator  
        a.send(None)
      # set a current measurement value, and then see how proportionl controller
      # responds to this value
      # caution: we need firstly start genrator or use next() and then do the following send  
        current_measurement = 25
        print(a.send(current_measurement))
      #######################################################################################
        #call PID control
        PID_simulation = controller.PID_simulation(controller.kp,controller.ki,controller.kd,controller.MV_initial)
        
        
        
