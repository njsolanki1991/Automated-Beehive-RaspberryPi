# The python script below serves the purpose of sensing the air quality inside the beehive which is very much indicative of the population 
# of bees inside the hive and also provides information of honey production. The gas of major importance here is carbon di oxide which is 
# measured in ppm and finally uploaded to the firebase database.

import time
import math
from MCP3008 import MCP3008

class MQ():

    ######################### Hardware Related Macros #########################
    MQ_PIN                       = 0        # Analog input channel of ADC MPC3008.
    RL_VALUE                     = 5        # Load resistence on the board in Kohms.
    RO_CLEAN_AIR_FACTOR          = 9.83     # Sensor resistance in clean air/RO which is derived from the chart in datasheet of MQ135.
 
    ######################### Software Related Macros #########################
    CALIBARAION_SAMPLE_TIMES     = 50       # Number of samples to be taken in calibration phase.
    CALIBRATION_SAMPLE_INTERVAL  = 500      # Time interval between each samples in calibration phase (milliseconds).
    READ_SAMPLE_INTERVAL         = 50       # Time interval between each samples in operation phase (milliseconds).
    READ_SAMPLE_TIMES            = 5        # Number of samples to be recorded in the operation phase.
 
    ######################### Application Related Macros ######################
    GAS_LPG                      = 0
    GAS_CO                       = 1
    GAS_SMOKE                    = 2
    
    def __init__(self, Ro=10, analogPin=0):
        self.Ro = Ro                        #Ro is resistence of the sensor in the clean air.
        self.MQ_PIN = analogPin             #The analog input pin for the readout of the sensor.
        self.adc = MCP3008()                #ADC function call created in MCP3008.py
    
    ############### Defining sensitivity characteristics of MQ135 ################
    # Along the horizontal axis you see the values 100, 1000 & 10000.
    # Between 100 & 1000 each vertical line adds 100, between 1000 & 10000 each vertical line adds 1000.
    # So we take the point P1 (x = 200, y = ~ 1.62) and P2 (x = 10000, y = ~ 0.26). 
    # To calculate the "real" values, we use the tens logarithm . 
    # Using the two-point form  we can calculate the slope, which in our case is -0.47.
    # With the slope and the drawn logarithm from the left point (x = 2.3, y = 0.21) we can now determine the line.
    
        self.LPGCurve = [2.3,0.21,-0.47]                            # Two points are taken from the sensitivity curve. 
                                                                    # with these two points, a line is formed which is "approximately equivalent"
                                                                    # to the original curve. 
                                                                    # data format:{ x, y, slope}; point1: (lg200, 0.21), point2: (lg10000, -0.59) 
        self.COCurve = [2.3,0.72,-0.34]     
                                            
        self.SmokeCurve =[2.3,0.53,-0.44]   
                                            
                                              
                
        print("Calibrating...")
        self.Ro = self.MQCalibration(self.MQ_PIN)                   # Sensor calibration with the readings read from MQ_PIN which is the analog input pin.
        print("Calibration is done...\n")
        print("Ro=%f kohm" % self.Ro)                               # Resistence of the sensor which has changed from intial assigned value to arbitrary 
                                                                    # value depending on ppm of the gases.
    
    
    def MQPercentage(self):
        val = {}
        read = self.MQRead(self.MQ_PIN)
        val["GAS_LPG"]  = self.MQGetGasPercentage(read/self.Ro, self.GAS_LPG)
        val["CO"]       = self.MQGetGasPercentage(read/self.Ro, self.GAS_CO)
        val["SMOKE"]    = self.MQGetGasPercentage(read/self.Ro, self.GAS_SMOKE)
        return val
        
    ######################### MQResistanceCalculation #########################
    # Varaible description:   raw_adc - Value read from adc, which represents the voltage.
    # Output:  The calculated sensor resistance
    # Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
    #          across the load resistor and its resistance, the resistance of the sensor
    #          could be derived.
    ############################################################################ 
    def MQResistanceCalculation(self, raw_adc):
        return float(self.RL_VALUE*(1023.0-raw_adc)/float(raw_adc));  # The concept behind the formula is as such 10-bit ADC assumes 5V (System Voltage)
                                                                      # is 1023 and anything less than 5V will be a ratio between 5V and 1023. 
     
     
    ######################### MQCalibration ####################################
    # Variable description:   mq_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It use  
    #          MQResistanceCalculation to calculates the sensor resistance in clean air 
    #          and then divides it with RO_CLEAN_AIR_FACTOR. 
    ############################################################################ 
    def MQCalibration(self, mq_pin):
        val = 0.0
        for i in range(self.CALIBARAION_SAMPLE_TIMES):                # Take multiple calibration samples
            val += self.MQResistanceCalculation(self.adc.read(mq_pin))
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
            
        val = val/self.CALIBARAION_SAMPLE_TIMES                       # calculate the average value

        val = val/self.RO_CLEAN_AIR_FACTOR                            # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                                      # according to the chart in the datasheet 

        return val;
      
      
    #########################  MQRead ##########################################
    # Variable description:   mq_pin - analog channel
    # Output:  rs of the sensor
    # Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
    #          The Rs changes as the sensor is in the different consentration of the target gas. 
    ############################################################################ 
    def MQRead(self, mq_pin):
        rs = 0.0

        for i in range(self.READ_SAMPLE_TIMES):
            rs += self.MQResistanceCalculation(self.adc.read(mq_pin)) 
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)

        rs = rs/self.READ_SAMPLE_TIMES

        return rs
     
    #########################  MQGetGasPercentage ##############################
    # Variable description:   rs_ro_ratio - Rs divided by Ro.
    #          gas_id      - target gas type.
    # Output:  ppm of the target gas.
    # Remarks: This function passes different curves to the MQGetPercentage function which 
    #          calculates the ppm (parts per million) of the target gas.
    ############################################################################ 
    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        if ( gas_id == self.GAS_LPG ):
            return self.MQGetPercentage(rs_ro_ratio, self.LPGCurve)
        elif ( gas_id == self.GAS_CO ):
            return self.MQGetPercentage(rs_ro_ratio, self.COCurve)
        elif ( gas_id == self.GAS_SMOKE ):
            return self.MQGetPercentage(rs_ro_ratio, self.SmokeCurve)
        return 0
     
    #########################  MQGetPercentage #################################
    # Variable description:   rs_ro_ratio - Rs divided by Ro
    #                         pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
    #          of the line could be derived if y(rs_ro_ratio) is provided. 
    ############################################################################ 
    def MQGetPercentage(self, rs_ro_ratio, pcurve):
        return (math.pow(10,( ((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0])))  
       

