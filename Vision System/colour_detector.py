import cv2
import numpy as np
import imutils
from stream_settings import Stream_Settings
from thresholds import Thresholds
class Colour_Detector():


    def __init__(self, object_handler, thresholds, use_trackbars=False, colours_to_detect=None):
        self.thresholds = thresholds
        self.use_trackbars = use_trackbars
        self.object_handler = object_handler
        self.colours = colours_to_detect # (LOWER, UPPER) : COLOUR_STRING.
        if(self.use_trackbars):
            self.add_trackbars()

    def add_colour(self, lower_threshold, upper_threshold, label):
        if(self.use_trackbars == False):
            if(self.colours != None):
                self.colours.update({(lower_threshold, upper_threshold) : label})
                
            else:
                self.colours = {}
                self.add_colour(lower_threshold, upper_threshold, label)



    def add_trackbars(self):
        def on_value_change(self):
                pass
        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 1000, 500)
        cv2.createTrackbar("HUE MIN", "Parameters", self.thresholds.HUE_MIN, self.thresholds.HUE_MAX, on_value_change)
        cv2.createTrackbar("HUE MAX", "Parameters", self.thresholds.HUE_MAX, self.thresholds.HUE_MAX, on_value_change)
        cv2.createTrackbar("SAT MIN", "Parameters", self.thresholds.SAT_MIN, self.thresholds.SAT_MAX, on_value_change)
        cv2.createTrackbar("SAT MAX", "Parameters", self.thresholds.SAT_MAX, self.thresholds.SAT_MAX, on_value_change)
        cv2.createTrackbar("VALUE MIN", "Parameters", self.thresholds.VALUE_MIN, self.thresholds.VALUE_MAX, on_value_change)
        cv2.createTrackbar("VALUE MAX", "Parameters", self.thresholds.VALUE_MAX, self.thresholds.VALUE_MAX, on_value_change)
        
  

    def detect(self, capture):
        if(self.use_trackbars):                
            self.thresholds.HUE_MIN = cv2.getTrackbarPos("HUE MIN", "Parameters")
            self.thresholds.SAT_MIN = cv2.getTrackbarPos("SAT MIN", "Parameters")
            self.thresholds.VALUE_MIN = cv2.getTrackbarPos("VALUE MIN", "Parameters")
            self.thresholds.HUE_MAX = cv2.getTrackbarPos("HUE MAX", "Parameters")
            self.thresholds.SAT_MAX = cv2.getTrackbarPos("SAT MAX", "Parameters")
            self.thresholds.VALUE_MAX = cv2.getTrackbarPos("VALUE MAX", "Parameters")
            self.colours = {((self.thresholds.HUE_MIN,self.thresholds.SAT_MIN,self.thresholds.VALUE_MIN), 
            (self.thresholds.HUE_MAX,self.thresholds.SAT_MAX,self.thresholds.VALUE_MAX)) : ""} # Default value             
             

        if(self.colours):
            #for Color enhancment
            capture = cv2.normalize(capture, None, alpha=-0.25, beta=1.2, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            # scale to uint8
            capture = np.clip(capture, 0, 1)
            capture = (255*capture).astype(np.uint8)

            hsv = cv2.cvtColor(capture, cv2.COLOR_RGB2HSV)
            bgr = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)

            masks = []
            mask = cv2.inRange(hsv, np.array(list(self.colours.items())[0][0][0]), 
            np.array((list(self.colours.items())[0][0][1]))) # First Mask
            

            # Establish The Individual Masks and preserve their colour
            for colour in self.colours:
                masks.append((cv2.inRange(bgr, np.array(colour[0]), np.array(colour[1])), self.colours[colour]))

            for colour in range(len(masks)):
                kernel = np.ones((self.thresholds.DILATION_KERNEL_MIN, self.thresholds.DILATION_KERNEL_MAX), np.uint8)
                dilated_mask = cv2.dilate(masks[colour][0], kernel, self.thresholds.DILATION_ITERATIONS_MIN)
                edge_detect = cv2.Canny(dilated_mask, self.thresholds.EDGE_THRESHOLD1, self.thresholds.EDGE_THRESHOLD2, None, 3)
                contours, _ = cv2.findContours(edge_detect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours_poly2 = [None]*len(contours)
                bbox = [None]*len(contours)
                for i, curves in enumerate(contours):
                    contours_poly2[i] = cv2.approxPolyDP(curves, 3, True)
                    bbox[i] = cv2.boundingRect(contours_poly2[i])

                for i in range(len(contours)):
                    area = cv2.contourArea(contours[i])
                    if(area > self.thresholds.AREA_MIN):
                        cv2.rectangle(capture, (int(bbox[i][0]), int(bbox[i][1])), (int(bbox[i][0]+bbox[i][2]), 
                        int(bbox[i][1]+bbox[i][3])), (255,255,255), 2)
                        # bbox_corner_pts = ((x,y), ((x+w), (y+h)))
                        # self.object_handler.add_corner_data(contours_poly2[i]))
                        # self.object_handler.add_coordinates_data((bbox_corner_pts[0][0], bbox_corner_pts[0][1], w, h))
                        # self.object_handler.add_boundaries()
                        # self.object_handler.add_colour_data(colour)
                        self.object_handler.add_object_to_list()
                        # cv2.putText(norm_img1, 'RED BUOY - Dangerous', (int(boundRect[i][0]), int(boundRect[i][1])), 1, 1, 
                        colour_detected_capture = cv2.bitwise_and(capture, capture, mask = masks[colour][0]) # Merge the original with the mask
                


            # Combine the masks into one colour mask
            # for colour in range(len(masks)):
            #     mask = mask + masks[colour][0]
                
            
            

            if(self.use_trackbars):
                # Send each mask to the contour detector (to detect that specific colour)
                # for mask in masks:
                #     self.__contour_detection(mask[0], mask[1])
                cv2.imshow("COLOUR DETECTOR", colour_detected_capture)     
           
            return colour_detected_capture


        else:
            print("No Colours To Detect!")
            exit()



    '''FOR TESTING PURPOSES ONLY'''
    def __contour_detection(self, capture, colour):
        conts = cv2.findContours(capture, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        conts = imutils.grab_contours(conts)            
        max_bbox = 0
        for c in conts:
            perimeter = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c, 0.02*perimeter, True) # Corner points
            bbox = cv2.boundingRect(approx)
            x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            bbox_pts = np.float32([[x,y], [x+w, y+h], [x+w, y], [x, y+h]]) # TL = x,y, TR = x+w, y, BL = x,y+h, BR = x+w, y+h

            center = (int(x+w/2),int(y+h/2)) # Center of bbox
            if(h > max_bbox):
                bbox_corner_pts = ((x,y), ((x+w), (y+h)))
                self.object_handler.add_corner_data(len(approx))
                self.object_handler.add_coordinates_data((bbox_corner_pts[0][0], bbox_corner_pts[0][1], w, h))
                self.object_handler.add_boundaries()
                self.object_handler.add_colour_data(colour)

                self.object_handler.add_object_to_list()
                max_bbox = h
                        
        
