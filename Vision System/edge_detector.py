import cv2
from stream_settings import Stream_Settings
from thresholds import Thresholds
import imutils
import numpy as np
class Edge_Detector():

    def __init__(self, object_handler, use_trackbars):
        self.use_trackbars = use_trackbars
        self.object_handler = object_handler
        

    def detect(self, capture):
        grey_scale = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        blur = self.blur(grey_scale)
        if(self.use_trackbars == True):
            Thresholds.EDGE_THRESHOLD1 = cv2.getTrackbarPos("EDGE THRESHOLD1", "Parameters") 
            Thresholds.EDGE_THRESHOLD2 = cv2.getTrackbarPos("EDGE THRESHOLD2", "Parameters")
            Thresholds.DILATION = cv2.getTrackbarPos("DILATION", "Parameters")
            Thresholds.EROSION = cv2.getTrackbarPos("EROSION", "Parameters")            
        edge_detector = cv2.Canny(blur, Thresholds.EDGE_THRESHOLD1, Thresholds.EDGE_THRESHOLD2)
        kernel = np.ones((5,5))
        dilate = cv2.dilate(edge_detector, kernel, iterations=Thresholds.DILATION)
        erode = cv2.erode(dilate, kernel, iterations=Thresholds.EROSION)
        edge_detected_capture = erode
        if(self.use_trackbars):
            cv2.imshow("Edge Detector", edge_detected_capture)
        self.__contour_detection(edge_detected_capture)
        


    def __contour_detection(self, capture):
        conts = cv2.findContours(capture, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        conts = imutils.grab_contours(conts)
        if(self.use_trackbars):
            Thresholds.AREA_MIN = cv2.getTrackbarPos("AREA MIN", "Parameters")
            Thresholds.AREA_MAX = cv2.getTrackbarPos("AREA MAX", "Parameters")
            Thresholds.CORNER_POINTS_MIN = cv2.getTrackbarPos("CORNER POINTS MIN", "Parameters")
            Thresholds.CORNER_POINTS_MAX = cv2.getTrackbarPos("CORNER POINTS MAX", "Parameters")
            
        max_bbox = 0
        for c in conts:
            perimeter = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c, 0.02*perimeter, True) # Corner points
            bbox = cv2.boundingRect(approx)
            x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            bbox_pts = np.float32([[x,y], [x+w, y+h], [x+w, y], [x, y+h]]) # TL = x,y, TR = x+w, y, BL = x,y+h, BR = x+w, y+h

            center = (int(x+w/2),int(y+h/2)) # Center of bbox
            
            # Reduce the detection so only a set size of objects can be detected
            if(cv2.contourArea(c) > Thresholds.AREA_MIN and cv2.contourArea(c) < Thresholds.AREA_MAX):
                # The buoys usually have 8 corner points
                if(len(approx) > Thresholds.CORNER_POINTS_MIN and len(approx) < Thresholds.CORNER_POINTS_MAX):
                    # Only display a box over the object itself and ignore all the shapes detected INSIDE the object itself
                    if(h > max_bbox):
                        bbox_corner_pts = ((x,y), ((x+w), (y+h)))
                        self.object_handler.add_corner_data(len(approx))
                        self.object_handler.add_coordinates_data((bbox_corner_pts[0][0], bbox_corner_pts[0][1], w, h))
                        # self.object_handler.add_coordinates_data(bbox)
                        self.object_handler.add_boundaries()
                        self.object_handler.add_object_to_list()
                        max_bbox = h
                        

    def blur(self, capture):
        return cv2.GaussianBlur(capture, (Thresholds.BLUR_KERNEL, Thresholds.BLUR_KERNEL_MAX), 1)


    
    def dilation(self, capture):
        kernel = np.ones((Thresholds.DILATION_KERNEL,Thresholds.DILATION_KERNEL_MAX)) # thickness
        if(self.use_trackbars):
            Thresholds.DILATION = cv2.getTrackbarPos("DILATION", "Parameters")
        return cv2.dilate(capture, kernel, iterations=Thresholds.DILATION)


    def erosion(self, capture):
        kernel = np.ones((Thresholds.EROSION_KERNEL,Thresholds.EROSION_KERNEL_MAX))
        if(self.use_trackbars):
            Thresholds.EROSION = cv2.getTrackbarPos("EROSION", "Parameters")
        return cv2.dilate(capture, kernel, iterations=Thresholds.EROSION)


