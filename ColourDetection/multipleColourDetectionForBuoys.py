#
# File: multipleColourDetectionForBuoys.py
# Author: Sitha Sinoun
# Email ID: sinsy077@mymail.unisa.edu.au

# Description: This program aims to help the RobotX boat detect 4 coloured buoys using openCV for multiple colour
# detection, the colours being red, white, green and black.
# For the RobotX boat to visualise the surrounding environment, detecting buoys and their colour in real-time will help
# complete the task of gate identification.

import cv2
import numpy as np

# Capturing the video stream through the webcam
cap = cv2.VideoCapture(0)

while True:

    # Reading the video steam from the webcam to capture frames
    ret, frame = cap.read()

    # Convert the frame(s) from BGR (RGB colour space) into HSV (hue, saturation, value)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Defines the upper and lower ranges for the colour red
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    # Defines the range of red colours into HSV,
    # the red_mask variable creates a mask of red coloured objects detected in the frame
    red_mask = cv2.inRange(hsv, red_lower, red_upper)

    # The bitwise function is performed between the frame and red_mask so that only the red coloured objects
    # are featured and stored in the variable red_result, other colours are discarded
    red_result = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Defines the upper and lower ranges for the colour green
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)

    # Defines the range of green colours into HSV,
    # the green_mask variable creates a mask of green coloured objects detected in the frame
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    # The bitwise function is performed between the frame and green_mask so that only the green coloured objects
    # are featured and stored in the variable green_result, other colours are discarded
    green_result = cv2.bitwise_and(frame, frame, mask=green_mask)

    # Defines the upper and lower ranges for the colour white
    white_lower = np.array([0, 0, 168], np.uint8)
    white_upper = np.array([172, 111, 255], np.uint8)

    # Defines the range of white colours into HSV,
    # the white_mask variable creates a mask of white coloured objects detected in the frame
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    # The bitwise function is performed between the frame and white_mask so that only the white coloured objects
    # are featured and stored in the variable white_result, other colours are discarded
    white_result = cv2.bitwise_and(frame, frame, mask=white_mask)

    # Defines the upper and lower ranges for the colour black
    black_lower = np.array([0, 0, 0], np.uint8)
    black_upper = np.array([180, 255, 30], np.uint8)

    # Defines the range of white colours into HSV,
    # the black_mask variable creates a mask of white coloured objects detected in the frame
    black_mask = cv2.inRange(hsv, black_lower, black_upper)

    # The bitwise function is performed between the frame and black_mask so that only the black coloured objects
    # are featured and stored in the variable black_result, other colours are discarded
    black_result = cv2.bitwise_and(frame, frame, mask=black_mask)

    # Create a contour to make the specific red coloured area more identifiable and distinguishable
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 500:
            # Constructing the size of boxes to be drawn around the detected red area
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 0, 255, 2))

            cv2.putText(frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    # Create a contour to make the specific green coloured area more identifiable and distinguishable
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 500:
            # Constructing the size of boxes to be drawn around the detected green area
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0, 2))

            cv2.putText(frame, "Green", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

    # Create a contour to make the specific white coloured area more identifiable and distinguishable
    contours, hierarchy = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 500:
            # Constructing the size of boxes to be drawn around the detected white area
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255, 2))

            cv2.putText(frame, "White", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))

    # Create a contour to make the specific black coloured area more identifiable and distinguishable
    contours, hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 500:
            # Constructing the size of boxes to be drawn around the detected black area
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0, 2))

            cv2.putText(frame, "Black", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0))

    # Displays the frame, mask and result of selected colours in separate windows
    cv2.imshow('Red, Green, White & Black Colour Detection', frame)
    cv2.imshow('red_mask', red_mask)
    cv2.imshow('red_result', red_result)
    cv2.imshow('green_mask', green_mask)
    cv2.imshow('green_result', green_result)
    cv2.imshow('white_mask', white_mask)
    cv2.imshow('white_result', white_result)
    cv2.imshow('black_mask', black_mask)
    cv2.imshow('black_result', black_result)

    # Terminates program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Eliminates all GUI Windows
cv2.destroyAllWindows()

# Releases captured frame
cap.release()









