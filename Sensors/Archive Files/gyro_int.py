#!/usr/bin/python
import smbus 
import math
import time
import datetime
import sys
from firebase import db

class Gyro_Acc_sensor:
    
    def RecordGyroAccData():
        
        # Register
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c
         
        def read_byte(reg):
            return bus.read_byte_data(address, reg)
         
        def read_word(reg):
            h = bus.read_byte_data(address, reg)
            l = bus.read_byte_data(address, reg+1)
            value = (h << 8) + l
            return value
         
        def read_word_2c(reg):
            val = read_word(reg)
            if (val >= 0x8000):
                return -((65535 - val) + 1)
            else:
                return val
         
        def dist(a,b):
            return math.sqrt((a*a)+(b*b))
         
        def get_y_rotation(x,y,z):
            radians = math.atan2(x, dist(y,z))
            return -math.degrees(radians)
         
        def get_x_rotation(x,y,z):
            radians = math.atan2(y, dist(x,z))
            return math.degrees(radians)
         
        bus = smbus.SMBus(1) # bus = smbus.smbus(0) fuer Revision 1 Change smbus.smbus(1) to smbus.SMBus(1) if error occurs
        address = 0x68       # via i2cdetect
         
        # Aktivieren, um das Modul ansprechen zu koennen
        bus.write_byte_data(address, power_mgmt_1, 0)
         
        print ("Gyroscope")
        print ("--------")
         
        gyroscope_xout = read_word_2c(0x43)
        gyroscope_yout = read_word_2c(0x45)
        gyroscope_zout = read_word_2c(0x47)
         
        print ("Gyro_xout: ", ("%5d" % gyroscope_xout))#, " scale: ", (gyroscope_xout / 131))
        print ("Gyro_yout: ", ("%5d" % gyroscope_yout))#, " scale: ", (gyroscope_yout / 131))
        print ("Gyro_zout: ", ("%5d" % gyroscope_zout))#, " scale: ", (gyroscope_zout / 131))
         
        print ()
        print ("Accelerometer")
        print ("---------------------")
         
        acceleration_xout = read_word_2c(0x3b)
        acceleration_yout = read_word_2c(0x3d)
        acceleration_zout = read_word_2c(0x3f)
         
        acceleration_xout_scale = acceleration_xout / 16384.0
        acceleration_yout_scale = acceleration_yout / 16384.0
        acceleration_zout_scale = acceleration_zout / 16384.0
         
        print ("Acceleration_xout: ", ("%6d" % acceleration_xout))#, " scale: ", acceleration_xout_scale)
        print ("Acceleration_yout: ", ("%6d" % acceleration_yout))#, " scale: ", acceleration_yout_scale)
        print ("Acceleration_zout: ", ("%6d" % acceleration_zout))#, " scale: ", acceleration_zout_scale)
         
        #print ("X Rotation: " , get_x_rotation(acceleration_xout_scale, acceleration_yout_scale, acceleration_zout_scale))
        #print ("Y Rotation: " , get_y_rotation(acceleration_xout_scale, acceleration_yout_scale, acceleration_zout_scale))

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
