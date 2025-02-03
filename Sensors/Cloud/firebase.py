#Program Description : This program deals with defining connection parameters to Firebase Database

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import time
import datetime

#Project ID is the name of the project set in Firebase Database; in our case it is 'raspi-acd09'
project_id = 'raspi-acd09' 

#Use the application default credentials

#Certificate is the private key generated in Firebase. To download the key follow below steps -
# 1.Go to Firebase project->Project Settings->Service Accounts->Generate Private KeyError
# 2.Save the json file generated to desired path and then provide the path in cred

cred = credentials.Certificate('/home/pi/PlanBee/raspi-acd09-firebase-adminsdk-udul0-6c64fc9126.json')			
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
  'storageBucket': 'raspi-acd09.appspot.com'				#Add the Link which is available in Firebase->Storage
})

db = firestore.client()										#To upload normal data to Database of Firebase
bucket = storage.bucket()									#To upload multimedia data to Storgae of Firebase

