import can
import frc
import time
import serial
import string
import pynmea2
import datetime

class GPS_Data:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        #self.sat_using = 0
        #self.pdop = 0
    
def parse_nmea(gps_data,nmea_sentence):   
    if nmea_sentence[0:6] == "$GPRMC"
        newmsg=pynmea2.parse(nmea_sentence)
        if not str(newmsg.lat):
            gps_data.lat = str(newmsg.latitude)
            gps_data.lon = str(newmsg.longitude)
    elif nmea_sentence[0:6] == "$GPGGA"
        # get satellites using
    elif nmea_sentence[0:6] == "$GPGSA"
        # get position dilution of precision (PDOP)

def transmit(gps_data):
    #send data to CAN-Bus
    #transformed_data = transform_into_CAN_Data(gps_data)
    #canlibrary.send(transformed_data)

def main():
    LOG_LOCATION = ""
    ENABLE_LOGGING = False 
    ser = serial.Serial('/dev/ttyACM0',9600)    
    NMEA_TYPES = ["$GPGGA","$GNGGA","$GPGSA","$GNGSA","$GPGSV"]
    
    current_data = GPS_Data()

    while True:
        newdata=ser.readline().decode('unicode_escape')
        parse_nmea(current_data,newdata)
        transmit(current_data)
        
        if ENABLE_LOGGING == True:
            if newdata[0:6] in NMEA_TYPES:
                with open(LOG_LOCATION+".csv", "a") as file:
                    file.write(newdata)
                    file.close()
            
def destroy():
    # Release resource

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()
