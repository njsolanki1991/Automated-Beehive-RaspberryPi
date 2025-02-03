import RPi.GPIO as GPIO
import time
import sys
import datetime
from firebase import db

class light_sensor:
    
    def RecordLightData(): #function for recording light Data
        
        GPIO.setmode(GPIO.BCM) #referring pins by Broadcom SOC model
        GPIO.setup(17,GPIO.IN) #setup pin 17 for input
        val= (GPIO.input(17)-1) * (-1)  # calculation of logic to compare where the door is open or not

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
