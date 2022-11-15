1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
# !/usr/bin/python3

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
<<<<<<< HEAD
        #print("got")
        #print(msg.arbitration_id)
=======
        # print("got")
        # print(msg.arbitration_id)
>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
        if (msg.arbitration_id != None):
            binVal = bin(msg.arbitration_id)

            if len(binVal) > 25:
                binVal = binVal[2:len(binVal)]
                while (len(binVal) < 29):
                    binVal = "0" + binVal
<<<<<<< HEAD
                deviceID = int(binVal[len(binVal)-6:len(binVal)],2)
                apiIndex = int(binVal[len(binVal)-10:len(binVal)-6],2)
                apiClass = int(binVal[len(binVal)-16:len(binVal)-10],2)
                manufacturerCode = int(binVal[len(binVal)-24:len(binVal)-16],2)
                deviceType = int(binVal[0:5],2)
=======
                deviceID = int(binVal[len(binVal) - 6:len(binVal)], 2)
                apiIndex = int(binVal[len(binVal) - 10:len(binVal) - 6], 2)
                apiClass = int(binVal[len(binVal) - 16:len(binVal) - 10], 2)
                manufacturerCode = int(binVal[len(binVal) - 24:len(binVal) - 16], 2)
                deviceType = int(binVal[0:5], 2)
>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
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
<<<<<<< HEAD
                        #print("Got one:" + str(deviceType))

                        if (deviceType == 12 and apiClass == 2):
                            #print("Weather report")
                            self.weatherReport.parse(msg)

                        if (deviceType == 14 and apiClass == 2):
                            #print("GPS report")
=======
                        # print("Got one:" + str(deviceType))

                        if (deviceType == 12 and apiClass == 2):
                            # print("Weather report")
                            self.weatherReport.parse(msg)

                        if (deviceType == 14 and apiClass == 2):
                            # print("GPS report")
>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
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
<<<<<<< HEAD
        msg = can.Message(is_extended_id=True, arbitration_id=canID, data = dataToSend)
=======
        msg = can.Message(is_extended_id=True, arbitration_id=canID, data=dataToSend)
>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
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
<<<<<<< HEAD
        canID = self.binLength(bin(deviceType),5) + self.binLength(bin(manufactureCode),8) + self.binLength(bin(apiIndex),6) + self.binLength(bin(apiCode),4) + self.binLength(bin(deviceID),6)
        return int(canID,2)
=======
        canID = self.binLength(bin(deviceType), 5) + self.binLength(bin(manufactureCode), 8) + self.binLength(
            bin(apiIndex), 6) + self.binLength(bin(apiCode), 4) + self.binLength(bin(deviceID), 6)
        return int(canID, 2)
>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e

    def binLength(self, binValue, bits):
        binValue = binValue[2:len(binValue)]
        while len(binValue) < bits:
            binValue = "0" + binValue
        return binValue

<<<<<<< HEAD
=======

>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
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
<<<<<<< HEAD
        self.pressure = int.from_bytes([msg.data[6],msg.data[7]], "big")
=======
        self.pressure = int.from_bytes([msg.data[6], msg.data[7]], "big")

>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e

class GpsCan:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.enabled = False

    def parse(self, msg):
<<<<<<< HEAD
        self.latitude = round(struct.unpack('>f', msg.data[0:4])[0],6)
        self.longitude = round(struct.unpack('>f', msg.data[4:8])[0],6)

    def generateCANData(self, lat, long):
        latValue  = int(round(lat  * 1000000))
=======
        self.latitude = round(struct.unpack('>f', msg.data[0:4])[0], 6)
        self.longitude = round(struct.unpack('>f', msg.data[4:8])[0], 6)

    def generateCANData(self, lat, long):
        latValue = int(round(lat * 1000000))
>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
        longValue = int(round(long * 1000000))
        data = latValue.to_bytes(4, "big") + longValue.to_bytes(4, "big")
        return data

<<<<<<< HEAD
=======

>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
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

<<<<<<< HEAD
=======

>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
class GateCan:
    def __init__(self):
        self.gateNumber = 0
        self.enabled = False

<<<<<<< HEAD
=======

>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
class MoveCan:
    def __init__(self):
        self.xVal = 0.0
        self.yVal = 0.0
        self.rVal = 0.0
        self.pVal = 0.0
        self.heading = 0
<<<<<<< HEAD
    
=======

>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
    def generateCANData(self, xVal, yVal, rVal, pVal):
        tempX = int(round(self.xVal * 1000)) + 2000
        tempY = int(round(self.yVal * 1000)) + 2000
        tempR = int(round(self.rVal * 1000)) + 2000
        tempP = int(round(self.pVal * 1000)) + 2000
        data = tempX.to_bytes(2, "big") + tempY.to_bytes(2, "big") + tempR.to_bytes(2, "big") + tempP.to_bytes(2, "big")
<<<<<<< HEAD
        return data
=======
        return data
>>>>>>> cb5e7d127edcd2d92f94997528676ec20dc11b8e
