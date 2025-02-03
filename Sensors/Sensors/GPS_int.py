import serial               #import serial pacakge
import time		    #import time package
import datetime		    #import date time package
import sys                  #import system package
from firebase import db


#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
        decimal_value = raw_value/100.00  			#divide by 100 to get the degree value from the NMEA format
        degrees = int(decimal_value)	  			#type casting to get just first two digit
        mm_mmmm = (decimal_value - int(decimal_value))/0.6  	# for getting the value after the decimal 
        position = degrees + mm_mmmm				#calculate the final value of the position in degrees
        position = "%.4f" %(position)				# format the value of position, here we get just 4 digits after decimal 
        return position						#value of the position is returned

class GPS_Record:
    
    def RecordGPSData():

        NMEA_buff = 0						#initialization of NMEA_buff because it may sometimes contain garbage value
        lat_in_degrees = 0					#initialization of latitude value
        long_in_degrees = 0					#initialization of longitude value
        gpgga_info = "$GPGGA,"					# we are reading GPGGA value from the GPS sensor
        ser = serial.Serial("/dev/ttyS0")                       #Open port with baud rate we can either select ttys0 or ttyAMA0 serial port
        GPGGA_buffer = 0					#initialization of GPGGA_buffer

        while True:     
            received_data = (str)(ser.readline())                   #A function is called so that it reads NMEA string received from the GPS sensor
            #print(received_data[1:10])
            GPGGA_data_available = received_data.find(gpgga_info)   #IT checks whether NMEA GPGGA string is avaiable or not
            #print(GPGGA_data_available)
            if (GPGGA_data_available>0):
                GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #it stores the data coming after "$GPGGA," string
                NMEA_buff = (GPGGA_buffer.split(','))               #the  data is stored in buffer which is separated by comma
                #global new_lat
                nmea_time = []
                nmea_latitude = []
                nmea_longitude = []
                nmea_time = NMEA_buff[0]                    # time is extracted from GPGGA string
                nmea_latitude = NMEA_buff[1]                # latitude value is extracted from GPGGA string and stored in nmea_latitude
                nmea_longitude = NMEA_buff[3]               # longitude value is extracted from GPGGA string and stored in nmea_longitude
                
                #print("NMEA Time: ", nmea_time,'\n')
                #print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
                
                lat = float(nmea_latitude)                  #conversion of string into float for calculation
                longi = float(nmea_longitude)               #conversion of string into float for calculation
                
                lat_in_degrees = convert_to_degrees(lat)    #conversion of  latitude in degree decimal format
                long_in_degrees = convert_to_degrees(longi) #conversion of longitude in degree decimal format
                
                print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees)
                #Send data to firebase
                data = {
                             "lat in degrees" : lat_in_degrees,
                             "long in degree": long_in_degrees
                        }
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
                doc_ref = db.collection(u'NEO_6M').document(st)
                doc_ref.set(data)
                exit(0)        

        
