"""
HX711 Load cell amplifier Python Library
Original source: https://gist.github.com/underdoeg/98a38b54f889fce2b237
Documentation source: https://github.com/aguegu/ardulibs/tree/master/hx711
Adapted by 2017 Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


##################
PYTHON 3 EXAMPLE

This version of example is python 3 compatible
and outputs weight in grams.

Make sure you enter the correct values for offset and scale!
Also, don't forget to set the correct gain, default is 128.
"""

import RPi.GPIO as GPIO
import time
import sys
from Load_Cells.hx711 import HX711
import datetime
from firebase import db



# Force Python 3 ###########################################################

if sys.version_info[0] != 3:
    raise Exception("Python 3 is required.")

############################################################################


hx = HX711(5, 6)

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def setup():
    """
    code run once
    """
    hx.set_offset(7888437.9375)
    hx.set_scale(-3428.71507424)


setup()
class Load_Cells:
    
    def RecordWeightData():

        try:
            val = hx.get_grams()
            #val2= (val)*8300/27 #with bag
            #print(val)
            #print(val2) # with bag
            val3= (val+5)*7.0/33.3 #with cartoon
            print('Weight of beehive = {} kg'.format(val3))

            hx.power_down()
            time.sleep(1)
            hx.power_up()
            time.sleep(2)
            #Send data to database
            data = {
                     "Beehive_weight_kg" : val3,
                   }
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
            doc_ref = db.collection(u'Load_Cells').document(st)
            doc_ref.set(data)
            
        except (KeyboardInterrupt, SystemExit):
            print("Exit")
            cleanAndExit()
