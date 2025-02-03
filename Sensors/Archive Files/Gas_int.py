from Gas_Sensor.mq import *
import sys, time, datetime
from firebase import db

class Gas_Sensor:
    
    def RecordGasData():
        
        try:
            #print("Press CTRL+C to abort.")
            
            mq = MQ();
           
            perc = mq.MQPercentage()
            #sys.stdout.write("\r")
            #sys.stdout.write("\033[K")
            sys.stdout.write("Methane: %g ppm, CO: %g ppm, Smoke: %g ppm\n" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
            sys.stdout.flush()


            #Send data to firebase
            data = {
                 "Methane" : perc["GAS_LPG"],
                 "C02": perc["CO"],
                 "Smoke": perc["SMOKE"]
                   }
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
            doc_ref = db.collection(u'MQ135').document(st)
            doc_ref.set(data)

        except:
            print("\nAbort by user")
