from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import os
import logging
import RPi.GPIO as GPIO

from Camera_int import camera_images
from Sound_int import usb_mic
from DHT_int import dht_temp_humidity
from light_int import light_sensor
from BME280_int import BME_sensor
from gyro_int import Gyro_Acc_sensor
from Gas_int import Gas_Sensor
from Load_Cells_int import Load_Cells
from GPS_int import GPS_Record


def light_switch():
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17,GPIO.IN)
        val= (GPIO.input(17)-1) * (-1)
        return(val)

#light = light_switch()
#print(light)

def add_jobs_set1():
        scheduler.add_job(light_sensor.RecordLightData, 'interval', seconds=10, id ='a1')
        scheduler.add_job(BME_sensor.RecordBMEData, 'interval', seconds=20, id ='a2')
        scheduler.add_job(Gas_Sensor.RecordGasData, 'interval', seconds=20, id ='a3')
        scheduler.add_job(dht_temp_humidity.RecordDHTData, 'interval', seconds=40, id ='a4')
        #scheduler.add_job(GPS_Record.RecordGPSData, 'interval', seconds=40, id ='a5'))
        #scheduler.add_job(Load_Cells.RecordWeightData, 'interval', seconds=50, id ='a6'))
        scheduler.add_job(Gyro_Acc_sensor.RecordGyroAccData, 'interval', seconds=70, id ='a7')
        scheduler.add_job(usb_mic.RecordSoundData, 'interval', seconds=80, id ='a8')
        scheduler.add_job(camera_images.RecordImageData, 'interval', seconds=90, id ='a9')

def add_jobs_set2():
        scheduler.add_job(light_sensor.RecordLightData, 'interval', seconds=15, id ='b1')
        scheduler.add_job(BME_sensor.RecordBMEData, 'interval', seconds=25, id ='b2')
        scheduler.add_job(Gas_Sensor.RecordGasData, 'interval', seconds=25, id ='b3')
        scheduler.add_job(dht_temp_humidity.RecordDHTData, 'interval', seconds=45, id ='b4')
        #scheduler.add_job(GPS_Record.RecordGPSData, 'interval', seconds=45, id ='b5'))
        #scheduler.add_job(Load_Cells.RecordWeightData, 'interval', seconds=55, id ='b6'))
        scheduler.add_job(Gyro_Acc_sensor.RecordGyroAccData, 'interval', seconds=75, id ='b7')
        scheduler.add_job(usb_mic.RecordSoundData, 'interval', seconds=85, id ='b8')
        scheduler.add_job(camera_images.RecordImageData, 'interval', seconds=95, id ='b9')
    

def remove_jobs_set1():
        scheduler.remove_job('a1')
        scheduler.remove_job('a2')
        scheduler.remove_job('a3')
        scheduler.remove_job('a4')
        #scheduler.remove_job('a5')
        #scheduler.remove_job('a6')
        scheduler.remove_job('a7')
        scheduler.remove_job('a8')
        scheduler.remove_job('a9')

def remove_jobs_set2():
        scheduler.remove_job('b1')
        scheduler.remove_job('b2')
        scheduler.remove_job('b3')
        scheduler.remove_job('b4')
        #scheduler.remove_job('b5')
        #scheduler.remove_job('b6')
        scheduler.remove_job('b7')
        scheduler.remove_job('b8')
        scheduler.remove_job('b9')
        

#Handler 
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG
fmt = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
#h = logging.StreamHandler()
h = logging.FileHandler('Start_Sensors_1.log')
h.setFormatter(fmt)
log.addHandler(h)

scheduler = BackgroundScheduler()
state1 = 0
state2 = 0
while True:
        #sleep(10)
        if light_switch() == 1:
            print('Open1')
            if state2 == 0:
                scheduler.start()
            else:
                scheduler.resume()
            add_jobs_set1()
            while True:
                sleep(10)
                if light_switch() == 0:
                    print('Close1')
                    state1 = 1
                    remove_jobs_set1()
                    scheduler.pause()
                    break
                
        elif light_switch() == 0:
            print('Close2')
            if state1 == 0:
                scheduler.start()
            else:
                scheduler.resume()
            add_jobs_set2()
            while True:
                sleep(10)
                if light_switch() == 1:
                    print('Open2')
                    state2 = 1
                    remove_jobs_set2()
                    scheduler.pause()
                    break