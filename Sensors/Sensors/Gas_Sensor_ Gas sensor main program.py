# Program Description:
# The python script is the file which should be run by the user as it incorporates all the scipts in the backend i.e mq.py and mcp3008. 
from mq import *                                                                    
import sys, time, datetime
from firebase import db
 
try:
    print("Press CTRL+C to abort.")                                     #In order to stop the recording of the sensor user has to press CTRL+C.
    mq = MQ();                                                          #Assigning of class MQ created in mq.py to the variable mq.
   # while True:                                                        #Displaying the percentage of the mixuture of gases sensed.
    perc = mq.MQPercentage()
    sys.stdout.write("\r")
    sys.stdout.write("\033[K")                                          #Sensing resistance obtained from the datasheet of MQ135.
    sys.stdout.write("Methane: %g ppm, CO: %g ppm, Smoke: %g ppm\n" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
    sys.stdout.flush()
#time.sleep(1)

                                                                        #Uploading the recorded data to the firebase database
    data = {
         "Methane" : perc["GAS_LPG"],
         "C02": perc["CO"],
         "Smoke": perc["SMOKE"]
           }
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')  #Embedding the time stamp of the recorded data.
    doc_ref = db.collection(u'MQ135').document(st)                      #Creating a branch in the collections for MQ135
    doc_ref.set(data)

except:
    print("\nAbort by user")