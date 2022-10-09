import cv2
import numpy as np
import keyboard

def on_value_change():
    pass


def track():
    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 1500, 1000)

    cv2.createTrackbar("HUE MIN", "Parameters", 0, 179, on_value_change)
    cv2.createTrackbar("SAT MIN", "Parameters", 255,255,on_value_change)
    cv2.createTrackbar("VALUE MIN", "Parameters", 255,255,on_value_change)



def colours():
    imgHSV = np.zeros((250, 500, 3), np.uint8)
    while True:
        imgHSV
        h = cv2.getTrackbarPos("HUE MIN", "Parameters")
        s = cv2.getTrackbarPos("SAT MIN", "Parameters")
        v = cv2.getTrackbarPos("VALUE MIN", "Parameters")

        imgHSV[:] = (h,s,v)
        img_brg = cv2.cvtColor(imgHSV, cv2.COLOR_HSV2BGR)

        cv2.imshow("HSV", img_brg)
        if cv2.waitKey(1) and keyboard.is_pressed("q"):
                         break


