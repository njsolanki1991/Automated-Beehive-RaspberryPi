#!/usr/bin/python
import smbus                                               # to access I2C SMBus module                           
import math
import time
import datetime
import sys
from firebase import db

class Gyro_Acc_sensor:                                      # Class to read the values of the Gyroscope and accelerometer
    
    def RecordGyroAccData():
        
        # Register                                           
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
         
        def read_byte(reg):                                 # this reads the data byte from the I2C device 
            return bus.read_byte_data(address, reg)         # address= address of the device to read data from,reg=register to be read
         
        def read_word(reg):                                 # this reads data word from the I2C device
            h = bus.read_byte_data(address, reg)            # read the higher data byte from the first register
            l = bus.read_byte_data(address, reg+1)          # lower data byte from the second register                                                 
            value = (h << 8) + l                            # Concatenate the values of both the register and is stored in value
            return value
         
        def read_word_2c(reg):                              # Converting into signed values
            val = read_word(reg)                            # Gyroscope and Accelerometer sensor 16-bit raw data are in 2's compliment form 
            if (val >= 0x8000):                             # this is converted to the usual signed form by comparing with the value 32768   
                return -((65535 - val) + 1)                 # as it is half of 65536 (2^16)
            else:
                return val
         
        def dist(a,b):                                      # this function calculates the distance of x,y,z from the origin
            return math.sqrt((a*a)+(b*b))
         
        def get_y_rotation(x,y,z):                         # Measure the tilt angle in y direction 
            radians = math.atan2(x, dist(y,z))
            return -math.degrees(radians)
         
        def get_x_rotation(x,y,z):                        # Measure the tilt angle in x direction
            radians = math.atan2(y, dist(x,z))
            return math.degrees(radians)
         
        bus = smbus.SMBus(1)                              # smbus.SMBus(1) is used for revision two boards                                                          
        address = 0x68                                    # address of the I2C device 
         
       
        bus.write_byte_data(address, power_mgmt_1, 0)     # Wake up MPU6050 as it starts in sleep mode
        
        print ("Gyroscope")
        print ("--------")
         
        gyroscope_xout = read_word_2c(0x43)               # The 16-bit 2'compliments raw data is stored in the register at the address 0x43,
        gyroscope_yout = read_word_2c(0x45)               # 0x45,0x47 these values are passes to read_word_2c function to convert it into 
        gyroscope_zout = read_word_2c(0x47)               # normal data form.
         
        print ("Gyro_xout: ", ("%5d" % gyroscope_xout), " scale: ", (gyroscope_xout / 131)) # the raw acceleration value obtained is scaled 
        print ("Gyro_yout: ", ("%5d" % gyroscope_yout), " scale: ", (gyroscope_yout / 131)) # by its sensivity factor 131
        print ("Gyro_zout: ", ("%5d" % gyroscope_zout), " scale: ", (gyroscope_zout / 131))
         
        print ()
        print ("Accelerometer")
        print ("---------------------")
         
        acceleration_xout = read_word_2c(0x3b)            # the 16-bit 2's compliment raw data is stored in the register at the address 0x3b
        acceleration_yout = read_word_2c(0x3d)            # 0x3d,0x3f these values are passed to read_word_2c function to convert it into 
        acceleration_zout = read_word_2c(0x3f)            # normal data
         
        acceleration_xout_scale = acceleration_xout / 16384.0  # the raw acceleration value obtained is scaled by its sensivity factor 1684
        acceleration_yout_scale = acceleration_yout / 16384.0
        acceleration_zout_scale = acceleration_zout / 16384.0
         
        print ("Acceleration_xout: ", ("%6d" % acceleration_xout))#, " scale: ", acceleration_xout_scale)
        print ("Acceleration_yout: ", ("%6d" % acceleration_yout))#, " scale: ", acceleration_yout_scale)
        print ("Acceleration_zout: ", ("%6d" % acceleration_zout))#, " scale: ", acceleration_zout_scale)
       

        #Send data to firebase
        data = {
         "Gyro_xout" : gyroscope_xout,
         "Gyro_yout": gyroscope_yout,
         "Gyro_zout" : gyroscope_zout,
         "Acceleration_xout" : acceleration_xout,
         "Acceleration_yout" : acceleration_yout,
         "Acceleration_zout" : acceleration_zout
           }
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
        doc_ref = db.collection(u'MPU_6050').document(st)
        doc_ref.set(data)
