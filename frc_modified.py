#!/usr/bin/python3

import os
import can
import struct
import random

class FrcCan(can.Listener):
    targets = []
    
    def __init__(self, channelID, bustypeName):
        print("sudo /sbin/ip link set " + channelID + " up type can bitrate 1000000")
        os.system("sudo /sbin/ip link set " + channelID + " up type can bitrate 1000000")
        #os.system('sudo ip link set ' + channelID + ' type can bitrate 100000')
        os.system('sudo ifconfig ' + channelID + ' down')
        os.system('sudo ifconfig ' + channelID + ' up')
        self.channel = channelID
        self.bus = can.interface.Bus(channel = self.channel, bustype = bustypeName)
        notifier = can.Notifier(self.bus, [self])
        
        self.weatherReport = WeatherCan()
        self.gpsPosition = GpsCan()
        self.systemMode = systemModeCan()
        self.uavStatus = uavStatusCan()
        self.entranceGate = entranceGateCan()
        self.exitGate = exitGateCan()
        self.followPathMsg = followPathCan()
        self.lightPattern = scanCodeCan()
        
    def on_message_received(self, msg):
        binVal = bin(msg.arbitration_id)
        deviceID = int(binVal[len(binVal)-6:len(binVal)],2)
        indexNo = int(binVal[len(binVal)-10:len(binVal)-6],2)
        apiClass = int(binVal[len(binVal)-16:len(binVal)-10],2)
        manufacturerCode = int(binVal[len(binVal)-24:len(binVal)-16],2)
        deviceType = int(binVal[2:6],2)
        #print(deviceID)
        #print(indexNo)
        #print(apiClass)
        #print(manufacturerCode)
        #print(deviceType)
        
        # Do we care?
        for target in self.targets:
            if (deviceType == target[0] and manufacturerCode == target[1]):
                #print("Got one")
                
                if (deviceType == 12 and apiClass == 2):
                    print("Weather report")
                    self.weatherReport.parse(msg)
                
                if (deviceType == 14 and apiClass == 2):
                    #print("GPS report")
                    self.gpsPosition.parse(msg)
                    
                # Below are mock CANs with substitued values for deviceType and apiClass
                
                if (deviceType == 15 and apiClass == 2):
                    #print("AMS System Mode")
                    self.systemMode.parse(msg)
                    
                if (deviceType == 16 and apiClass == 2):
                    #print("Current UAV Status")
                    self.uavStatus.parse(msg)
                    
                if (deviceType == 17 and apiClass == 2):
                    #print("Active Entrance Gate")
                    self.entranceGate.parse(msg)
                    
                if (deviceType == 18 and apiClass == 2):
                    #print("Active Exit Gate")
                    self.exitGate.parse(msg)
                    
                if (deviceType == 19 and apiClass == 2):
                    #print("Follow the Path Status")
                    self.followPathMsg.parse(msg)
                    
                if (deviceType == 20 and apiClass == 2):
                    #print("Light Pattern Color")
                    self.lightPattern.parse(msg)

        can.Logger("recorded.log")
        
    def sendMessage(self, deviceType, manufactureCode, apiIndex, apiCode, deviceID):
        canID = self.generateCanID(deviceType, manufactureCode, apiIndex, apiCode, deviceID)
        msg = can.Message(is_extended_id=True, arbitration_id=canID, data=[0])
        self.bus.send(msg)
        
    def generateCanID(self, deviceType, manufactureCode, apiIndex, apiCode, deviceID):
        canID = self.binLength(bin(deviceType),5) + self.binLength(bin(manufactureCode),8) + self.binLength(bin(apiIndex),6) + self.binLength(bin(apiCode),4) + self.binLength(bin(deviceID),6)
        return int(canID,2)
        
    def binLength(self, binValue, bits):
        binValue = binValue[2:len(binValue)]
        while len(binValue) < bits:
            binValue = "0" + binValue
        return binValue
        
class WeatherCan:
    def __init__(self):
        self.windDirection = 0
        self.windSpeed = 0.0
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        
    def parse(self, msg):
        self.windDirection = int.from_bytes([msg.data[0],msg.data[1]], "big")
        self.windSpeed = int.from_bytes([msg.data[2],msg.data[3]], "big") / 100.0
        self.temperature = msg.data[4]
        self.humidity = msg.data[5]
        self.pressure = int.from_bytes([msg.data[6],msg.data[7]], "big")     
        
class GpsCan:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        
    def parse(self, msg):
        self.latitude = round(struct.unpack('>f', msg.data[0:4])[0],6)
        self.longitude = round(struct.unpack('>f', msg.data[4:8])[0],6)


# Since there is no data on the ardruino, the following below Mock Can classes have no real data
# to parse from potential single board computers that woube be connected via Can Bus

class systemModeCan:
    def __init__(self):
        
        self.remoteOperated = 1
        self.autonomous = 2
        self.killed = 3
    
    # for testing purposes
    def parse(self, msg):
        
        self.remoteOperated = 1
        self.autonomous = 2
        self.killed = 3
        
class uavStatusCan:
    def __init__(self):
        
        self.stowed = 1
        self.deployed = 2
        self.faulted = 3

class entranceGateCan:
    def __init__(self):
        
        self.entryGateOne = 1
        self.entryGateTwo = 2
        self.entryGateThree = 3
        
class exitGateCan:
    def __init__(self):
        self.exitGateOne = 1
        self.exitGateTwo = 2
        self.exitGateThree = 3

class followPathCan:
    def __init__(self):
        
        self.inProgress = 1
        self.completed = 2

class scanCodeCan():
    def __init__(self):
        
        self.red = "R"
        self.blue = "B"
        self.green = "G"
        



    
        