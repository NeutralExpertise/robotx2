import RPi.GPIO as GPIO
import drivers
import time

slidePin = 17
display = drivers.Lcd()

# Define a setup function for some setup
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(slidePin, GPIO.IN)

def main():
    while True:
        # slide switch high, led1 on
        if GPIO.input(slidePin) == 1:
            display.lcd_clear() 
            print ('GPS ACTIVE ')
            display.lcd_display_string('GPS ACTIVE',1)

        # slide switch low, led2 on
        if GPIO.input(slidePin) == 0:
            display.lcd_clear() 
            print ('GPS INACTIVE')
            display.lcd_display_string('GPS INACTIVE',1)
        time.sleep(0.5)

def destroy():
    # Release resource
    GPIO.cleanup()

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program
    # destroy() will be  executed.
    except KeyboardInterrupt:
        display.lcd_clear()
        destroy()