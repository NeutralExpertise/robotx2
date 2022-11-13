#!/usr/bin/python3

# File: objectDetectionRobotx.py
# Author: Sitha Sinoun
# EmailID: sinsy077@mymail.unisa.edu.au

# Description: This program is an Object Detection program for testing in the Maritime Robotx competition 2022.
# The program combines Opencv with a YOLOv5 deep learning object detection trained model.  It aims and is trained
# to detect 5 classes, which are a WAM-V boat, and four separate coloured buoys that are red, green, black and white.
# The program can be tested via streaming through a webcam or loading a video to detect the desired robotx objects.

import cv2
import numpy as np

# capturing the stream through a video (or webcam)
cap = cv2.VideoCapture('buoy_test2.mkv')
# loads yolov5 dnn model of robotx data
net = cv2.dnn.readNetFromONNX('best.onnx')
# loads all classes robot.onnx model can detect
file = open("robotx_classes.txt", "r")
# places all the labelled classes in a python list
classes = file.read().split('\n')
print(classes)

# while loop to access the frame(s) of the video or webcam
while True:

    # reading the video stream to capture frames
    ret, frame = cap.read()
    # conditional statement to ascertain whether frames are being gathered
    if frame is None:
        break
    # feed our model with the images from the video or webcam
    # create a blob to preprocess images for deep learning classification and detect objects
    # scale factor normalises image pixels, mean subtraction set to zero, swapRB=true swaps BGR to RGB, no cropping
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255, size=(640, 640), mean=[0, 0, 0], swapRB=True, crop=False)
    # provides the blob for the yolov5 robot model
    net.setInput(blob)
    # run the reference and gives Numpy ndarray as output which can be used to plot box on the given input image.
    detections = net.forward()[0]
    # FOR TESTING ONLY:  predicts 25200 bounding boxes and 85 column entries per bounding box
    # print(detections.shape)

    # first 2 positions for e.g, cx.cy are the centre of the bounding box, w, h, confidence value, 80 class_scores
    # find class_ids, confidences score, bounding_boxes

    classes_ids = []
    confidences = []
    bounding_boxes = []
    rows = detections.shape[0]

    # find width and length
    frame_width, frame_height = frame.shape[1], frame.shape[0]
    x_scale = frame_width/640
    y_scale = frame_height/640

    # showing information on the screen
    for i in range(rows):
        row = detections[i]
        confidence = row[4]
        if confidence > 0.5:

            # object detected
            classes_score = row[5:]
            index = np.argmax(classes_score)
            if classes_score[index] > 0.5:
                classes_ids.append(index)
                confidences.append(confidence)
                cx, cy, w, h = row[:4]

                # rectangle coordinates
                x1 = int((cx-w/2) * x_scale)
                y1 = int((cy-h/2) * y_scale)
                width = int(w * x_scale)
                height = int(h * y_scale)
                box = np.array([x1, y1, width, height])
                bounding_boxes.append(box)

    # removes redundant bounding boxes
    indices = cv2.dnn.NMSBoxes(bounding_boxes, confidences, 0.5, 0.5)

    for i in indices:

        x1, y1, w, h = bounding_boxes[i]
        label = classes[classes_ids[i]]
        conf = confidences[i]
        text = label + "{:.2f}".format(conf)

        # if object detected is a boat, bounding box is blue and text is pink
        if label == "boat":
            cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), (255, 0, 0), 2)
            cv2.putText(frame, text, (x1, y1-2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)

        # if object detected is a red buoy, bounding box is red and text is red
        elif label == "red_buoy":
            cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), (0, 0, 255), 2)
            cv2.putText(frame, text, (x1, y1-2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

        # if object detected is a black buoy, bounding box is black and text is black
        elif label == "black_buoy":
            cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), (0, 0, 0), 2)
            cv2.putText(frame, text, (x1, y1-2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)

        # if object detected is a green buoy, bounding box is green and text is green
        elif label == "green_buoy":
            cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), (0, 255, 0), 2)
            cv2.putText(frame, text, (x1, y1-2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

        # if object detected is a white buoy, bounding box is white and text is white
        elif label == "white_buoy":
            cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), (255, 255, 255), 2)
            cv2.putText(frame, text, (x1, y1-2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

    # displays the frame(s) or video in a GUI window
    cv2.imshow("ROBOTX_VIDEO_FRAME", frame)
    # terminates program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




