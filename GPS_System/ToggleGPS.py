import RPi.GPIO as GPIO
import drivers
import time
import serial
import string
import pynmea2
import datetime

data_form = 1
slide_pin = 17
prev_state = 0

DEBUG = True
ENABLE_LOGGING = True

display = drivers.Lcd()

# GPIO input setup
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(slide_pin, GPIO.IN)

def main():
    global data_form
    global prev_state
    
    while True:
        port="/dev/ttyAMA0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata=ser.readline().decode('unicode_escape')
        
        # Slide switch high
        if GPIO.input(slide_pin) == 1:
            if newdata[0:6] == "$GPRMC":
                try:
                    display.lcd_clear()
                    newmsg=pynmea2.parse(newdata)
                    gps_lat = str(newmsg.latitude)
                    gps_lon = str(newmsg.longitude)
                    gps_coord = gps_lat+ "," +gps_lon

                    display.lcd_display_string("Lat= " +gps_lat,1)
                    display.lcd_display_string("Lon= " +gps_lon,2)
                    
                    if DEBUG == True:
                        debug_log = "gpsdata" +str(data_form)+".csv  |  Lat=" +gps_lat+ " and Long=" +gps_lon+ \
                        "  |  " +str(newmsg)+ "  |  " +str(datetime.datetime.now())+ "\n"
                        print(debug_log)
                        with open("testData/debug.txt", "a") as file:
                            file.write(debug_log)
                            file.close()
                
                    if ENABLE_LOGGING == True:
                        with open("testData/gpsdata" + str(data_form) +".csv", "a") as file:
                            file.write(str(gps_coord) + "\n")
                            file.close()
                except (OSError, NameError) as err:
                    print(f"Unexpected {err=}, {type(err)=}")
                    display.lcd_display_string(f"{err=}",1)
                except ChecksumError:
                    print("Checksum Error")
                    with open("testData/gpsdata" + str(data_form) +".csv", "a") as file:
                            file.write("---------------Checksum Error!------------------\n")
                            file.close()                
                
                prev_state = 1
            
            elif newdata[0:6] == "$GPGSV":
                print("GPGSV Data: " +str(newdata))
                with open("testData/gpsdata" + str(data_form) +".csv", "a") as file:
                            file.write(str(newdata) + "\n")
                            file.close()
            else:
                print("Something went wrong. Data:" +str(newdata))

        #Slide switch low
        if GPIO.input(slide_pin) == 0:
            if prev_state == 1:
                try:
                    display.lcd_clear()
                except (OSError, NameError):
                    print("NameError/OSError: LCD Module likely disconnected")
                data_form += 1
            
            try:
                display.lcd_display_string('GPS INACTIVE',1)
            except (OSError, NameError):
                    print("NameError/OSError: LCD Module likely disconnected")
            
            print('GPS INACTIVE')
            prev_state = 0
        
        time.sleep(0.5)

def destroy():
    # Release resource
    GPIO.cleanup()
    display.lcd_clear()

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program
    # destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()