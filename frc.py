#!/usr/bin/python3

import os
import vision_can
import struct

class FrcCan(vision_can.Listener):
    targets = []
    
    def __init__(self, channelID, bustypeName):
        print("sudo /sbin/ip link set " + channelID + " up type can bitrate 1000000")
        os.system("sudo /sbin/ip link set " + channelID + " up type can bitrate 1000000")
        #os.system('sudo ip link set ' + channelID + ' type can bitrate 100000')
        os.system('sudo ifconfig ' + channelID + ' down')
        os.system('sudo ifconfig ' + channelID + ' up')
        self.channel = channelID
        self.bus = vision_can.interface.Bus(channel = self.channel, bustype = bustypeName)
        notifier = vision_can.Notifier(self.bus, [self])
        
        self.weatherReport = WeatherCan()
        self.gpsPosition = GpsCan()
        
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

        vision_can.Logger("recorded.log")
        
    def sendMessage(self, deviceType, manufactureCode, apiIndex, apiCode, deviceID):
        canID = self.generateCanID(deviceType, manufactureCode, apiIndex, apiCode, deviceID)
        msg = vision_can.Message(is_extended_id=True, arbitration_id=canID, data=[0])
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
        
    
        