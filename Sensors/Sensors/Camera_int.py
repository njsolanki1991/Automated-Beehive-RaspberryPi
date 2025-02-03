from picamera import PiCamera
from firebase import bucket
import sys
import time 
import datetime

camera = PiCamera()

class camera_images:
    
    def RecordImageData():
        
        #Setting Image properties
        
        #camera.rotation = 180
        camera.resolution = (1920, 1080)
        #camera.framerate = 15

        #Start Preview-- Remove if not required
        #camera.start_preview(alpha=255) #alpha = transparency

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')

        #Capture image
        camera.capture('/home/pi/Downloads/image%s.jpg' % st)

        #Send to Firebase Storage
        blob = bucket.blob('images/Image%s.jpg' % st)
        outfile='/home/pi/Downloads/image%s.jpg' % st
        with open(outfile, 'rb') as my_file:
            blob.upload_from_file(my_file)

        #Stop Preview - Remove if not required
        #camera.stop_preview()
