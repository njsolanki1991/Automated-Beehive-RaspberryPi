from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import os
import logging

from Camera_int import camera_images
from Sound_int import usb_mic
from DHT_int import dht_temp_humidity
from light_int import light_sensor
from BME280_int import BME_sensor
from gyro_int import Gyro_Acc_sensor
from Gas_int import Gas_Sensor
from Load_Cells_int import Load_Cells
from GPS_int import GPS_Record


#Handler 
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

scheduler = BackgroundScheduler()
scheduler.add_job(light_sensor.RecordLightData, 'interval', seconds=10)
scheduler.add_job(BME_sensor.RecordBMEData, 'interval', seconds=20)
scheduler.add_job(Gas_Sensor.RecordGasData, 'interval', seconds=20)
scheduler.add_job(dht_temp_humidity.RecordDHTData, 'interval', seconds=40)
scheduler.add_job(GPS_Record.RecordGPSData, 'interval', seconds=40)
scheduler.add_job(Load_Cells.RecordWeightData, 'interval', seconds=50)
scheduler.add_job(Gyro_Acc_sensor.RecordGyroAccData, 'interval', seconds=70)
scheduler.add_job(usb_mic.RecordSoundData, 'interval', seconds=80)
scheduler.add_job(camera_images.RecordImageData, 'interval', seconds=90)



scheduler.start()

##comment in to activate
while True:
    sleep(10)
