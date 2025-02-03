import Adafruit_DHT as dht
import time
import datetime
import sys
from firebase import db

class dht_temp_humidity:
    
    def RecordDHTData():
        
        #Set DATA pin
        DHT = 4

        #Read Temp and Hum from DHT22
        h,t = dht.read_retry(dht.DHT22, DHT)

        #Print Temperature and Humidity on Shell window
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))

        #Send data to firebase
        data = {
                 "Beehive_temp" : t,
                 "Beehive_humidity": h
               }
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
        doc_ref = db.collection(u'DHT22').document(st)
        doc_ref.set(data)
