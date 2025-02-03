import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import time
import datetime


project_id = 'raspi-acd09' 

# Use the application default credentials
cred = credentials.Certificate('/home/pi/PlanBee/raspi-acd09-firebase-adminsdk-udul0-6c64fc9126.json')
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
  'storageBucket': 'raspi-acd09.appspot.com'
})

db = firestore.client()

bucket = storage.bucket()

##file = '/home/pi/Downloads/Logo_Plan_Bee-02-02.jpg'


##ts = time.time()
##st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
##doc_ref = db.collection(u'sensor_data').document(st)
##doc_ref.set({
##    u'first': u'Gero',
##    u'last': u'Camp',
##    u'born': 2019
##})
