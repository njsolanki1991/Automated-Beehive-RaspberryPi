#This sensor DHT22 is used to measure relative humidity and temperature inside the beehive.
#Following program will give the relative humidity in the range of 0-100% with 2-5% accuracy and temperature -40 to 80 C with +/- 0.5 C accuracy.
#In this program we are using Adafruit_DHT library which we have to install before running the program.


import Adafruit_DHT as dht                                                 # run this "sudo pip3 install Adafruit_DHT" to install Adafruit_DHT library                 
import time
import datetime
import sys
from firebase import db

class dht_temp_humidity:
    
    def RecordDHTData():                                                     
        

        DHT = 4                                                             # Here we have to mention the GPIO pin number where we have connected output cable from sensor                                                                   # which we have to mention below
        
         
        h,t = dht.read_retry(dht.DHT22, DHT)                                # Read Temperature and Humidity from DHT22 using read_retry method
                                                                            # which will try up to 15 times to get sensor value, where h=humidity and t=temperature

        
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))            # Print Temperature and Humidity on Shell window
                                                                            # format the temperature and humidity to 1 decimal point 

        #Send data to firebase
        data = {
                 "Beehive_temp" : t,
                 "Beehive_humidity": h
               }
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
        doc_ref = db.collection(u'DHT22').document(st)
        doc_ref.set(data)
