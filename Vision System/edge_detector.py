import cv2
import imutils
import numpy as np
class Edge_Detector:

    def __init__(self, object_handler, thresholds, use_trackbars):
        self.use_trackbars = use_trackbars
        self.object_handler = object_handler
        self.thresholds = thresholds
        if(self.use_trackbars):
            self.add_trackbars()




    def add_trackbars(self):
        def on_value_change(self):
                pass
        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 1000, 500)
        cv2.createTrackbar("EDGE THRESHOLD 1", "Parameters", self.thresholds.EDGE_THRESHOLD1, self.thresholds.EDGE_THRESHOLD2, on_value_change)
        cv2.createTrackbar("EDGE THRESHOLD 2", "Parameters", self.thresholds.EDGE_THRESHOLD2, self.thresholds.EDGE_THRESHOLD2, on_value_change)
        cv2.createTrackbar("CORNERS MIN", "Parameters", self.thresholds.CORNER_POINTS_MIN, self.thresholds.CORNER_POINTS_MAX, on_value_change)
        cv2.createTrackbar("CORNERS MAX", "Parameters", self.thresholds.CORNER_POINTS_MAX, self.thresholds.CORNER_POINTS_MAX, on_value_change)
        cv2.createTrackbar("AREA MIN", "Parameters", self.thresholds.AREA_MIN, self.thresholds.AREA_MAX, on_value_change)
        cv2.createTrackbar("AREA MAX", "Parameters", self.thresholds.AREA_MAX, self.thresholds.AREA_MAX, on_value_change)
        cv2.createTrackbar("DILATION KERNEL MIN", "Parameters", self.thresholds.DILATION_KERNEL_MIN, self.thresholds.DILATION_KERNEL_MAX, on_value_change)
        cv2.createTrackbar("DILATION KERNEL MAX", "Parameters", self.thresholds.DILATION_KERNEL_MAX, self.thresholds.DILATION_KERNEL_MAX, on_value_change)
        cv2.createTrackbar("EROSION KERNEL MIN", "Parameters", self.thresholds.EROSION_KERNEL_MIN, self.thresholds.EROSION_KERNEL_MAX, on_value_change)
        cv2.createTrackbar("EROSION KERNEL MAX", "Parameters", self.thresholds.EROSION_KERNEL_MAX, self.thresholds.EROSION_KERNEL_MAX, on_value_change)
        cv2.createTrackbar("DILATION ITERATIONS", "Parameters", self.thresholds.DILATION_ITERATIONS_MIN, self.thresholds.DILATION_ITERATIONS_MAX, on_value_change)
        cv2.createTrackbar("EROSION ITERATIONS", "Parameters", self.thresholds.EROSION_ITERATIONS_MIN, self.thresholds.EROSION_ITERATIONS_MAX, on_value_change)
        


    def blur(self, capture):
        return cv2.GaussianBlur(capture, (self.thresholds.BLUR_KERNEL_MIN, self.thresholds.BLUR_KERNEL_MAX), 1)


    
    def dilation(self, capture):
        kernel = np.ones((self.thresholds.DILATION_KERNEL_MIN,self.thresholds.DILATION_KERNEL_MAX), np.uint8) # thickness            
        return cv2.dilate(capture, kernel, iterations=self.thresholds.DILATION_ITERATIONS_MIN)


    def erosion(self, capture):
        kernel = np.ones((self.thresholds.EROSION_KERNEL_MIN,self.thresholds.EROSION_KERNEL_MAX))
        return cv2.dilate(capture, kernel, iterations=self.thresholds.EROSION_ITERATIONS_MIN)
        

    def detect(self, capture):
        if(self.use_trackbars):                
            self.thresholds.EDGE_THRESHOLD1 = cv2.getTrackbarPos("EDGE THRESHOLD 1", "Parameters")
            self.thresholds.EDGE_THRESHOLD2 = cv2.getTrackbarPos("EDGE THRESHOLD 2", "Parameters")
            self.thresholds.CORNER_POINTS_MIN = cv2.getTrackbarPos("CORNERS MIN", "Parameters")
            self.thresholds.CORNER_POINTS_MAX = cv2.getTrackbarPos("CORNERS MAX", "Parameters")
            self.thresholds.AREA_MIN = cv2.getTrackbarPos("AREA MIN", "Parameters")
            self.thresholds.AREA_MAX = cv2.getTrackbarPos("AREA MAX", "Parameters")
            self.thresholds.EROSION_ITERATIONS_MIN = cv2.getTrackbarPos("EROSION ITERATIONS", "Parameters")
            self.thresholds.DILATION_ITERATIONS_MIN = cv2.getTrackbarPos("DILATION ITERATIONS", "Parameters")
            self.thresholds.DILATION_KERNEL_MIN = cv2.getTrackbarPos("DILATION KERNEL MIN", "Parameters")
            self.thresholds.DILATION_KERNEL_MAX = cv2.getTrackbarPos("DILATION KERNEL MAX", "Parameters")
            self.thresholds.EROSION_KERNEL_MIN = cv2.getTrackbarPos("EROSION KERNEL MIN", "Parameters")
            self.thresholds.EROSION_KERNEL_MAX = cv2.getTrackbarPos("EROSION KERNEL MAX", "Parameters")

        grey_scale = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        blur = self.blur(grey_scale)          
        edge_detector = cv2.Canny(blur, self.thresholds.EDGE_THRESHOLD1, self.thresholds.EDGE_THRESHOLD2)
        kernel = np.ones((self.thresholds.DILATION_KERNEL_MIN,self.thresholds.DILATION_KERNEL_MAX))
        dilate = cv2.dilate(edge_detector, kernel, iterations=self.thresholds.DILATION_ITERATIONS_MIN)
        erode = cv2.erode(dilate, kernel, iterations=self.thresholds.EROSION_ITERATIONS_MIN)
        edge_detected_capture = erode

        if(self.use_trackbars):
            cv2.imshow("Edge Detector", edge_detected_capture)

        self.__contour_detection(edge_detected_capture)
        


    def __contour_detection(self, capture):
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
            
            # Reduce the detection so only a set size of objects can be detected
            if(cv2.contourArea(c) > self.thresholds.AREA_MIN and cv2.contourArea(c) < self.thresholds.AREA_MAX):
                # The buoys usually have 8 corner points
                if(len(approx) > self.thresholds.CORNER_POINTS_MIN and len(approx) < self.thresholds.CORNER_POINTS_MAX):
                    # Only display a box over the object itself and ignore all the shapes detected INSIDE the object itself
                    if(h > max_bbox):
                        bbox_corner_pts = ((x,y), ((x+w), (y+h)))
                        self.object_handler.add_corner_data(len(approx))
                        self.object_handler.add_coordinates_data((bbox_corner_pts[0][0], bbox_corner_pts[0][1], w, h))
                        # self.object_handler.add_coordinates_data(bbox)
                        self.object_handler.add_boundaries()
                        self.object_handler.add_object_to_list()
                        max_bbox = h
                        
        
                        




