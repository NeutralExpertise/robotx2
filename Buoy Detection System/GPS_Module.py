#!/usr/bin/python3

# File: GPS_Module.py
# Author: Jeremiah Ye
# EmailID: yeyjb001@mymail.unisa.edu.au

# Description:  This program gets the serial output from the GPS module and converts it into decimal degrees and then
#               transmits it across the CAN bus. It listens to itself on the CAN Bus.
#               Log location and captured NMEA sentence type can be adjusted.

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


def initialise_can():
    global canBus
    canBus = frc.FrcCan('can0', 'socketcan')
    # GPS Listener
    canBus.targets.append([14, 8, 2])


def parse_nmea(gps_data, nmea_sentence):
    if nmea_sentence[0:6] == "$GPRMC":
        new_msg = pynmea2.parse(nmea_sentence)
        if not str(new_msg.lat):
            gps_data.lat = str(new_msg.latitude)
            gps_data.lon = str(new_msg.longitude)


def transmit(gps_data):
    data = canBus.gpsPosition.generateCANData(gps_data.lat, gps_data.lon)
    canBus.sendMessageWithData(14, 8, 2, 0, 2, data)


def main():
    LOG_LOCATION = ''
    ENABLE_LOGGING = False
    ser = serial.Serial('/dev/ttyACM0', 9600)
    NMEA_TYPES = ["$GPGGA", "$GNGGA", "$GPGSA", "$GNGSA", "$GPGSV", "$GPRMC"]

    current_data = GPS_Data()

    while True:
        try:
            new_data = ser.readline().decode('unicode_escape')
            parse_nmea(current_data, new_data)
        except pynmea2.ParseError:
            new_data = ''
        except pynmea2.SentenceTypeError:
            new_data = ''
        except pynmea2.ChecksumError:
            new_data = ''

        transmit(current_data)

        if ENABLE_LOGGING == True:
            if new_data[0:6] in NMEA_TYPES:
                with open(LOG_LOCATION + ".csv", "a") as file:
                    file.write(new_data)
                    file.close()


# If run this script directly, do:
if __name__ == '__main__':
    main()
