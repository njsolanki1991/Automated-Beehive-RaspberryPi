import RPi.GPIO as GPIO
import time
import sys
import datetime
from firebase import db

class light_sensor:
    
    def RecordLightData():
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17,GPIO.IN)
        val= (GPIO.input(17)-1) * (-1)

        #print output on Shell window
        if val==1:
                print("Door is Open")
        else:
                print("Door is Closed")

        #Send data to firebase
        data = {"light" : val}
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
        doc_ref = db.collection(u'kwmobile').document(st)
        doc_ref.set(data) 