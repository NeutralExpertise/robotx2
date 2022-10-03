import time
import board
import busio
import digitalio
import serial
import string
import pynmea2
from datetime import datetime
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from collections import deque
   
# Initialise global variables
def setup():
    #Display setup
    global font
    global oled
    global draw
    global image
    
    global ser
    global data_form
    global toggle_gps
    global prev_state
    global loading_bar
    
    global WIDTH
    global HEIGHT
    global LOOPTIME
    global current_time
    
    global DEBUG
    global DEBUG_LOGGING
    global ENABLE_LOGGING
    global DEBUG_LOC
    global GPSDATA_LOC
    
    data_form = 1
    toggle_gps = 17
    prev_state = 0
    loading_bar = deque(maxlen=20)

    WIDTH = 128
    HEIGHT = 64
    LOOPTIME = 0.2
    
    DEBUG = True
    DEBUG_LOGGING = True
    ENABLE_LOGGING = False 
    
    ser=serial.Serial("/dev/ttyAMA0")
    DEBUG_LOC = "/home/jeremiahye/Desktop/GPS_Test/testData/debug.txt"
    GPSDATA_LOC = "/home/jeremiahye/Desktop/GPS_Test/testData/gpsdata"

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(toggle_gps, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, board.I2C(), addr=0x3C, reset=digitalio.DigitalInOut(board.D4))       
    # Create blank image for drawing.
    image = Image.new("1", (oled.width, oled.height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
    font = ImageFont.truetype('PixelOperator.ttf', 16)

def oled_display(line_1='default line 1', line_2='default line 2', line_3='default line 3',line_4='default line 4'):
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    
    draw.text((0, 0), line_1, font=font, fill=255)
    draw.text((0, 16), line_2, font=font, fill=255)
    draw.text((0, 32), line_3, font=font, fill=255)
    draw.text((0, 48), line_4, font=font, fill=255)
    
    oled.image(image)
    oled.show()
    
def main():
    global ENABLE_LOGGING
    while True:     
        dataout = pynmea2.NMEAStreamReader()
        try:
            newdata=ser.readline().decode('unicode_escape')
        except:
            print("Serial Exception")    
        
        if GPIO.input(toggle_gps) == 1:
            GPIO.wait_for_edge(toggle_gps, GPIO.FALLING)
            ENABLE_LOGGING = not ENABLE_LOGGING
        
        if ENABLE_LOGGING == True:                          
            if newdata[0:6] == "$GPGGA" or newdata[0:6] == "$GPGSA" or newdata[0:6] == "$GPGSV":
                with open("testData/trifecta.csv", "a") as file:
                    file.write(newdata)
                    file.close()
                
                if loading_bar.count('|') < 20:
                    loading_bar.append('|')
                else:
                    loading_bar.clear()
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                oled_display("Writing to CSV",'['+''.join(loading_bar)+']',"",current_time)
            
            
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            oled_display('GPS Inactive','','',current_time)
            
def destroy():
    # Release resource
    GPIO.cleanup()
    #clear display

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program
    # destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()
        
#def discard_anom():
#0.00008993 = 10m
    
def save_log(log_data,log_location,log_type):
    if log_type == "DEBUG":
        with open(DEBUG_LOC, "a") as file:
            file.write(debug_log)
            file.close()
    elif log_type == "RECORD":
        pass
    elif log_type == "ERROR":
        pass
    
    with open(GPSDATA_LOC + str(data_form) +".csv", "a") as file:
        file.write(str(newdata) + "\n")
        file.close()
    