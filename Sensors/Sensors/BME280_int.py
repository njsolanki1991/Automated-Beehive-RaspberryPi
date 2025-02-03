import bme280 #sudo pip3 install RPi.bme280
import smbus2 #sudo pip3 install smbus2
import time
import datetime
import sys
from firebase import db


class BME_sensor:
    
    def RecordBMEData():
        
        port = 1
        address = 0x76 # Adafruit BME280 address. Other BME280s may be different
        bus = smbus2.SMBus(port)

        bme280.load_calibration_params(bus,address)


        bme280_data = bme280.sample(bus,address)
        humidity  = bme280_data.humidity
        pressure  = bme280_data.pressure
        ambient_temperature = bme280_data.temperature

        # Output data to screen
        print("Temperature in Celsius : {} C ".format(ambient_temperature))
        print("Pressure : {} hPa".format(pressure)) 
        print("Relative Humidity : ", humidity)

        #Send data to firebase
        data = {
         "Outside_temp" : ambient_temperature,
         "Outside_humidity": humidity,
         "Outside_pressure" : pressure
           }
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
        doc_ref = db.collection(u'BME280').document(st)
        doc_ref.set(data)
