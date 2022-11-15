#!/usr/bin/python3

import os

import can
import struct


class FrcCan(can.Listener):
    targets = []

    def __init__(self, channelID, bustypeName):
        print("sudo /sbin/ip link set " + channelID + " up type can bitrate 1000000")
        os.system("sudo /sbin/ip link set " + channelID + " up type can bitrate 1000000")
        # os.system('sudo ip link set ' + channelID + ' type can bitrate 100000')
        os.system('sudo ifconfig ' + channelID + ' down')
        os.system('sudo ifconfig ' + channelID + ' up')
        self.channel = channelID
        self.bus = can.interface.Bus(channel=self.channel, bustype=bustypeName)
        notifier = can.Notifier(self.bus, [self])

        self.weatherReport = WeatherCan()
        self.gpsPosition = GpsCan()
        self.movePosition = MoveCan()
        self.shooter = ShooterCan()
        self.gate = GateCan()

    def on_message_received(self, msg):
        # print("got")
        # print(msg.arbitration_id)
        if (msg.arbitration_id != None):
            binVal = bin(msg.arbitration_id)

            if len(binVal) > 25:
                binVal = binVal[2:len(binVal)]
                while (len(binVal) < 29):
                    binVal = "0" + binVal
                deviceID = int(binVal[len(binVal) - 6:len(binVal)], 2)
                apiIndex = int(binVal[len(binVal) - 10:len(binVal) - 6], 2)
                apiClass = int(binVal[len(binVal) - 16:len(binVal) - 10], 2)
                manufacturerCode = int(binVal[len(binVal) - 24:len(binVal) - 16], 2)
                deviceType = int(binVal[0:5], 2)
                if (deviceType == 16):
                    print(deviceType)
                    print(manufacturerCode)
                    print(apiIndex)
                    print(apiClass)
                    print(deviceID)
                    print(binVal)

                # Do we care?
                for target in self.targets:
                    if (deviceType == target[0] and manufacturerCode == target[1]):
                        # print("Got one:" + str(deviceType))

                        if (deviceType == 12 and apiClass == 2):
                            # print("Weather report")
                            self.weatherReport.parse(msg)

                        if (deviceType == 14 and apiClass == 2):
                            # print("GPS report")
                            self.gpsPosition.parse(msg)

                        if (deviceType == 16 and deviceID == 1 and apiClass == 1):
                            print("Shooter data")
                            self.shooter.setCANStatus(apiIndex)

        can.Logger("recorded.log")

    def sendMessage(self, deviceType, manufactureCode, apiIndex, apiCode, deviceID):
        canID = self.generateCanID(deviceType, manufactureCode, apiIndex, apiCode, deviceID)
        msg = can.Message(is_extended_id=True, arbitration_id=canID, data=[0])
        self.bus.send(msg)

    def sendMessageWithData(self, deviceType, manufactureCode, apiIndex, apiCode, deviceID, dataToSend):
        canID = self.generateCanID(deviceType, manufactureCode, apiIndex, apiCode, deviceID)
        msg = can.Message(is_extended_id=True, arbitration_id=canID, data=dataToSend)
        self.bus.send(msg)

    def sendShootMessage(self, deviceType, manufactureCode, apiIndex, apiCode, deviceID, rpm):
        canID = self.generateCanID(deviceType, manufactureCode, apiIndex, apiCode, deviceID)
        print(canID)
        if (rpm > 0):
            data = rpm.to_bytes(2, "big")
        print(data[0])
        msg = can.Message(is_extended_id=True, arbitration_id=canID, data=data)
        self.bus.send(msg)

    def generateCanID(self, deviceType, manufactureCode, apiIndex, apiCode, deviceID):
        canID = self.binLength(bin(deviceType), 5) + self.binLength(bin(manufactureCode), 8) + self.binLength(
            bin(apiIndex), 6) + self.binLength(bin(apiCode), 4) + self.binLength(bin(deviceID), 6)
        return int(canID, 2)

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
        self.windDirection = int.from_bytes([msg.data[0], msg.data[1]], "big")
        self.windSpeed = int.from_bytes([msg.data[2], msg.data[3]], "big") / 100.0
        self.temperature = msg.data[4]
        self.humidity = msg.data[5]
        self.pressure = int.from_bytes([msg.data[6], msg.data[7]], "big")


class GpsCan:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.enabled = False

    def parse(self, msg):
        self.latitude = round(struct.unpack('>f', msg.data[0:4])[0], 6)
        self.longitude = round(struct.unpack('>f', msg.data[4:8])[0], 6)

    def generateCANData(self, lat, long):
        latValue = int(round(lat * 1000000))
        longValue = int(round(long * 1000000))
        data = latValue.to_bytes(4, "big") + longValue.to_bytes(4, "big")
        return data


class ShooterCan:
    def __init__(self):
        self.enabled = False
        self.colorSequence = False
        self.docking = False
        self.targetColor = ""
        self.shooting = False

    def getRPMData(self, rpm):
        data = [0]
        if (rpm > 0):
            data = rpm.to_bytes(2, "big")
        return data

    def setCANStatus(self, apiIndex):
        if (apiIndex == 1):
            self.enabled = True
            self.colorSequence = False
            self.docking = False
            self.shooting = False
        if (apiIndex == 2):
            self.enabled = False
            self.colorSequence = False
            self.docking = False
            self.shooting = False
        elif (apiIndex == 3):
            self.enabled = True
            self.colorSequence = True
            self.docking = False
            self.shooting = False
        elif (apiIndex == 4):
            self.enabled = True
            self.colorSequence = False
            self.docking = True
            self.shooting = False
        elif (apiIndex == 5):
            self.enabled = True
            self.colorSequence = False
            self.docking = False
            self.shooting = True

    def generateCANStatusData(self):
        if (self.enabled == False):
            return 2
        elif (self.colorSequence):
            return 3
        elif (self.docking):
            return 4
        elif (self.shooting):
            return 5
        else:
            return 1


class GateCan:
    def __init__(self):
        self.gateNumber = 0
        self.enabled = False


class MoveCan:
    def __init__(self):
        self.xVal = 0.0
        self.yVal = 0.0
        self.rVal = 0.0
        self.pVal = 0.0
        self.heading = 0

    def generateCANData(self, xVal, yVal, rVal, pVal):
        tempX = int(round(self.xVal * 1000)) + 2000
        tempY = int(round(self.yVal * 1000)) + 2000
        tempR = int(round(self.rVal * 1000)) + 2000
        tempP = int(round(self.pVal * 1000)) + 2000
        data = tempX.to_bytes(2, "big") + tempY.to_bytes(2, "big") + tempR.to_bytes(2, "big") + tempP.to_bytes(2, "big")
        return data