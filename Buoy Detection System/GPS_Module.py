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
        # self.sat_using = 0
        # self.pdop = 0
    
def parse_nmea(gps_data,nmea_sentence):   
    if nmea_sentence[0:6] == "$GPRMC":
        newmsg=pynmea2.parse(nmea_sentence)
        if not str(newmsg.lat):
            gps_data.lat = str(newmsg.latitude)
            gps_data.lon = str(newmsg.longitude)
    # elif nmea_sentence[0:6] == "$GPGGA":
        # get satellites using
    # elif nmea_sentence[0:6] == "$GPGSA":
        # get position dilution of precision (PDOP)

def transmit(gps_data):
    #send data to CAN-Bus
    #transformed_data = transform_into_CAN_Data(gps_data)
    #
    #canlibrary.sendMsg(a,b,c,d,e, canBus.gpsPosition.generateDate())

def main():
    LOG_LOCATION = ""
    ENABLE_LOGGING = False 
    ser = serial.Serial('/dev/ttyACM0',9600)    
    NMEA_TYPES = ["$GPGGA","$GNGGA","$GPGSA","$GNGSA","$GPGSV","$GPRMC"]
    
    current_data = GPS_Data()

    while True:
        try:
            new_data = ser.readline().decode('unicode_escape')
            parse_nmea(current_data,new_data)
        except pynmea2.ParseError:
            new_data = ''
        except pynmea2.SentenceTypeError:
            new_data = ''
        except pynmea2.ChecksumError:
            new_data = ''

        transmit(current_data)

        if ENABLE_LOGGING == True:
            if new_data[0:6] in NMEA_TYPES:
                with open(LOG_LOCATION+".csv", "a") as file:
                    file.write(new_data)
                    file.close()

# If run this script directly, do:
if __name__ == '__main__':
    main()
