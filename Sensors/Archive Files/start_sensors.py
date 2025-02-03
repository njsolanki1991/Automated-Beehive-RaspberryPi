from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import os
from Camera_int import camera_images
from Sound_int import usb_mic


scheduler = BackgroundScheduler()

##scheduler.add_job(camera_images.RecordImageData, 'interval', seconds=15)
##scheduler.add_job(usb_mic.RecordSoundData, 'interval', seconds=10)


scheduler.start()

##comment in to activate
while True:
    sleep(10)