import cv2

import numpy as np
# using camera 0
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    # 1- convert frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2- define the range of red
    lower_red = np.array([-10, 100, 100])
    upper_red = np.array([10, 255, 255])

    # check if the HSV of the frame is lower or upper red
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    result = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Draw rectangular bounded line on the detected red area
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300): # to remove the noise
            # Constructing the size of boxes to be drawn around the detected red area
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)

    cv2.imshow("Tracking Red Colour", frame)
    cv2.imshow("Mask", red_mask)
    cv2.imshow("And", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
