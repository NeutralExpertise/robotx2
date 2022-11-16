#!/usr/bin/python3

# File: heartbeatMessage.py
# Author: Sitha Sinoun
# EmailID: sinsy077@mymail.unisa.edu.au

# Description:  This program aims to send a Heartbeat message at a frequency of 1hz to the Technical Director's Network for
#               the Maritime Robotx Competition and also acts as a Server for TCP/IP communications.  The Heartbeat message is formatted as
#               an NVEA-like sentence and this communication channel is used to relay information specific to a task during it's run attempt.
#               Heartbeat message fields contain data on GPS co-ordinates, AMS status, UAV status and the current date and time in AEDT- Sydney.
#               Most data fields are relayed from a position on a CAN device, and accessor methods are used to display those fields.

import time
from datetime import datetime
# pytz library allows accurate and cross timezone calculations
from pytz import timezone
import sys
import os
import can
import socket


sys.path.append(os.getcwd() + '/..')

import frc

def main():



    # instantiates a Can Bus listener
    canBus = frc.FrcCan('can0', 'socketcan');
    # appends the GPS Can
    canBus.targets.append([14,8,0]);
    # Note:  CanBus should append other Cans devices/locations such as UAV status
    #         and AMS system for the heartbeat message fields, however these Can
    #         locations are currently undefined/unknown.

    # converts time into AEDT
    aedt_tz = timezone('Australia/Sydney')
    datetime.now(aedt_tz)

    # initial Variables for the Heartbeat Message Fields
    message_id = ""
    latitude = 0.0
    north_south_indicator = ""
    longitude = 0.0
    east_west_indicator = ""
    team_id = ""
    system_mode = "0"
    uav_status = "0"
    checksum = "0"

    # enable server communications via socket module
    
    # host reserved for a given IP address, however field can remain empty throughout
    host = ''
    # reserve a port on our computer, can be anything
    port = 5000

    # instatiate a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind to the port number
    # an empty string in the ip field enables the server
    # to listen to requests coming from other
    # computers on the network
    s.bind((host, port))

    # start on the on listening mode
    s.listen(5)

    # accept the socket response from the client, and get the connection object
    c, addr = s.accept() # Note: execution waits here until the client calls s.connect()
    
    # will display the IP address of the client to verify connection
    print("CONNECTION FROM:", str(addr))


    # infinite loop to show heartbeat message fields until interrupted or an error occurs
    while 1:
            
        message_id = "$RXHRB"
        # gets latitude on the GPS Can from frc 
        latitude = str(canBus.gpsPosition.latitude)
        north_south_indicator = "N"
        # gets longitude on the GPS Can from frc
        longitude = str(canBus.gpsPosition.longitude)
        east_west_indicator = "W"
        team_id = "ROBOT"
        # Ideally, get the AMS mode from the system mode Can in frc, but no Can data to parse, therefore hardcoded
        system_mode = str(canBus.systemMode.autonomous)
        # ideally, get the drone status from the UAV Can in frc, but no Can data to parse, therefore hardcoded
        uav_status = str(canBus.uavStatus.deployed) + "*"
        # checksum is hardcoded, as I don't how to get checksum
        checksum = "3C"
        
        # condition statement to determine which direction GPS co-ordinates are facing
        if str(0) <= str(latitude) <= str(90):
            north_south_indicator = "N"
        else:
            north_south_indicator = "S"

        if str(0) <= str(longitude) <= str(180):
            east_west_indicator = "E"
        else:
            east_west_indicator = "W"    
        
        # ascertains AEDT current day, month, year and placed in variables
        current_datetime = datetime.now(aedt_tz)
        current_day = str(current_datetime)[8:10]
        current_month = str(current_datetime.month)
        current_year = str(current_datetime.year)[2:4]
        
        # ascertains AEDT-Sydney cuurent second, minute, hour and placed in variables
        sydney_hour = str(current_datetime)[11:13]
        sydney_minute = str(current_datetime)[14:16]
        sydney_second = str(current_datetime)[17:19]
        
        # final varibales for AEDT date and current time
        aedt_date = current_day + current_month + current_year
        aedt_time = sydney_hour + sydney_minute + sydney_second
        
        # generates heartbeat message, NMEA like sentence
        msg = ("Heartbeat Message = " + message_id + "," + aedt_date + "," + aedt_time + "," + latitude + "," + north_south_indicator
        + "," + longitude + "," + east_west_indicator + "," + team_id + "," + system_mode + "," + uav_status + checksum)
        
        # refreshes heartbeat message at a rate of 1Hz/1 second
        time.sleep(1)
        
        # sends the heartbeat message, encoding to send byte type
        c.send(msg.encode())

    #close the connection with the client
    c.close()

if __name__ == '__main__':
    
    main()
