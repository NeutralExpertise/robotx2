#!/usr/bin/python3
#
# simple_rx_test.py
# 
# This is simple CAN receive python program. All messages received are printed out on screen.
# For use with PiCAN boards on the Raspberry Pi
# http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-2-p-1475.html
#
# Make sure Python-CAN is installed first http://skpang.co.uk/blog/archives/1220
#
# 01-02-16 SK Pang
#
#
#

import can
import time
import os
import frc


print('\n\rCAN Rx test')
print('Bring up CAN0....')

time.sleep(0.1)

canBus = frc.FrcCan('can0', 'socketcan');
canBus.targets.append([14,8,0]);

print('Ready')

try:
    while True:
        time.sleep(2)
        print("Latitude:", end='\t')
        print(canBus.gpsPosition.latitude)
        print("Longitude:", end='\t')
        print(canBus.gpsPosition.longitude)

except KeyboardInterrupt:
    #Catch keyboard interrupt
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rKeyboard interupt')
    
