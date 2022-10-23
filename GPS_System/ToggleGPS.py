import sys
sys.path.append(r'/home/jeremiahye/.local/lib/python3.9/site-packages')
import time
import board
import busio
import digitalio
import serial
import string
import pynmea2
import datetime
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
    
    global ser_1
    global ser_2
    global ser_3
    global data_form
    global toggle_gps
    global prev_state
    global loading_bar
    
    global WIDTH
    global HEIGHT
    global current_time
    global TIME_END
    
    global DEBUG
    global DEBUG_LOGGING
    global ENABLE_LOGGING
    global DEBUG_LOC
    global GPSDATA_LOC
    global NMEA_TYPES
    
    data_form = 0
    toggle_gps = 17
    prev_state = 0
    loading_bar = deque(maxlen=20)

    WIDTH = 128
    HEIGHT = 64
    
    DEBUG = True
    DEBUG_LOGGING = True
    ENABLE_LOGGING = False 
    
    ser_1 = serial.Serial("/dev/ttyAMA0",9600)
    ser_3 = serial.Serial("/dev/ttyACM0",9600)
    
    DEBUG_LOC = "/home/jeremiahye/Desktop/GPS_Test/testData/debug"
    GPSDATA_LOC = "/home/jeremiahye/Desktop/GPS_Test/testData/gpsdata"
    
    NMEA_TYPES = ["$GPGGA","$GNGGA","$GPGSA","$GNGSA","$GPGSV"]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(toggle_gps, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, board.I2C(), addr=0x3C, reset=digitalio.DigitalInOut(board.D4))       
    # Create blank image for drawing.
    image = Image.new("1", (oled.width, oled.height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
    font = ImageFont.truetype('/home/jeremiahye/Desktop/GPS_Test/PixelOperator.ttf', 16)

def oled_display(line_1='default line 1', line_2='default line 2', line_3='default line 3',line_4='default line 4'):
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    
    draw.text((0, 0), line_1, font=font, fill=255)
    draw.text((0, 16), line_2, font=font, fill=255)
    draw.text((0, 32), line_3, font=font, fill=255)
    draw.text((0, 48), line_4, font=font, fill=255)
    
    oled.image(image)
    oled.show()
    
    
def parse_nmea(log_data):   
    newmsg=pynmea2.parse(log_data)
    if not str(newmsg.lat):
        gps_lat = str(newmsg.latitude)
        gps_lon = str(newmsg.longitude)
        gps_coord = gps_lat+ "," +gps_lon
        print(gps_coord)    
    
def log_file(nmea_sentence,source_num):
    if nmea_sentence[0:6] in NMEA_TYPES:
        with open(DEBUG_LOC+ "_" +str(source_num)+ ".csv", "a") as file:
            file.write(nmea_sentence)
            file.close()

        with open(GPSDATA_LOC+str(data_form)+"_"+str(source_num)+".csv", "a") as file:
            file.write(nmea_sentence)
            file.close()
            
        if nmea_sentence[0:6] == "$GNGGA" or nmea_sentence[0:6] == "$GPGGA":
            print(nmea_sentence)

def main():
    global ENABLE_LOGGING
    global data_form
    global prev_state 
    while True:
        #dataout = pynmea2.NMEAStreamReader() 
        if GPIO.input(toggle_gps) == 1:
            GPIO.wait_for_edge(toggle_gps, GPIO.FALLING)
            ENABLE_LOGGING = not ENABLE_LOGGING
            if ENABLE_LOGGING == True:
                ser_1.reset_input_buffer()
                ser_3.reset_input_buffer()
                TIME_END = time.time() + 3600
                now = datetime.datetime.now((datetime.timezone.utc))
                current_time = now.strftime("%H:%M:%S")
                print("Current Time: " +current_time+ " Time End: " +time.asctime(time.localtime((TIME_END))))
                with open(DEBUG_LOC+ "_x.csv", "a") as file:
                    file.write("Current Time:" +current_time)
                    file.close()
        
        if ENABLE_LOGGING == True:
            while ser_1.in_waiting > 0:
                newdata_1=ser_1.readline().decode('unicode_escape')
                log_file(newdata_1,1)
            while ser_3.in_waiting > 0:
                newdata_3=ser_3.readline().decode('unicode_escape')
                log_file(newdata_3,3)
   
            if loading_bar.count('|') < 20:
                loading_bar.append('|')
            else:
                loading_bar.clear()
                
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            oled_display("Writing to:","gpsdata"+str(data_form)+".csv",'['+''.join(loading_bar)+']',current_time)
            prev_state = 1
            
            if time.time() > TIME_END:
                ENABLE_LOGGING = False
            
        else:
            if prev_state == 1:
                data_form += 1
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            oled_display('GPS Inactive','','',current_time)
            prev_state = 0
            
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