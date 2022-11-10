import numpy as np
import cv2
import imutils
class Object_Detector:


    def __init__(self, object_handler, thresholds, colours_to_detect, use_trackbars=False):
        self.thresholds = thresholds
        self.use_trackbars = use_trackbars
        self.object_handler = object_handler
        self.colours = colours_to_detect # (LOWER, UPPER) : COLOUR_STRING.
        if(self.use_trackbars):
            self.add_trackbars()

    def add_colour(self, lower_threshold, upper_threshold, label):
            if(self.colours != None):
                self.colours.update({(lower_threshold, upper_threshold) : label})
                
            else:
                self.colours = {}
                self.add_colour(lower_threshold, upper_threshold, label)



    def add_trackbars(self):
        def on_value_change(self):
                pass
        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 1000, 700)
        cv2.createTrackbar("HUE MIN", "Parameters", self.thresholds.HUE_MIN, self.thresholds.HUE_MAX, on_value_change)
        cv2.createTrackbar("HUE MAX", "Parameters", self.thresholds.HUE_MAX, self.thresholds.HUE_MAX, on_value_change)
        cv2.createTrackbar("SAT MIN", "Parameters", self.thresholds.SAT_MIN, self.thresholds.SAT_MAX, on_value_change)
        cv2.createTrackbar("SAT MAX", "Parameters", self.thresholds.SAT_MAX, self.thresholds.SAT_MAX, on_value_change)
        cv2.createTrackbar("VALUE MIN", "Parameters", self.thresholds.VALUE_MIN, self.thresholds.VALUE_MAX, on_value_change)
        cv2.createTrackbar("VALUE MAX", "Parameters", self.thresholds.VALUE_MAX, self.thresholds.VALUE_MAX, on_value_change)
        # cv2.createTrackbar("EDGE THRESHOLD 1", "Parameters", self.thresholds.EDGE_THRESHOLD1, self.thresholds.EDGE_THRESHOLD2, on_value_change)
        # cv2.createTrackbar("EDGE THRESHOLD 2", "Parameters", self.thresholds.EDGE_THRESHOLD2, self.thresholds.EDGE_THRESHOLD2, on_value_change)
        # cv2.createTrackbar("CORNERS MIN", "Parameters", self.thresholds.CORNER_POINTS_MIN, self.thresholds.CORNER_POINTS_MAX, on_value_change)
        # cv2.createTrackbar("CORNERS MAX", "Parameters", self.thresholds.CORNER_POINTS_MAX, self.thresholds.CORNER_POINTS_MAX, on_value_change)
        cv2.createTrackbar("AREA MIN", "Parameters", self.thresholds.AREA_MIN, self.thresholds.AREA_MAX, on_value_change)
        cv2.createTrackbar("AREA MAX", "Parameters", self.thresholds.AREA_MAX, self.thresholds.AREA_MAX, on_value_change)
        # cv2.createTrackbar("DILATION KERNEL MIN", "Parameters", self.thresholds.DILATION_KERNEL_MIN, self.thresholds.DILATION_KERNEL_MAX, on_value_change)
        # cv2.createTrackbar("DILATION KERNEL MAX", "Parameters", self.thresholds.DILATION_KERNEL_MAX, self.thresholds.DILATION_KERNEL_MAX, on_value_change)
        # cv2.createTrackbar("EROSION KERNEL MIN", "Parameters", self.thresholds.EROSION_KERNEL_MIN, self.thresholds.EROSION_KERNEL_MAX, on_value_change)
        # cv2.createTrackbar("EROSION KERNEL MAX", "Parameters", self.thresholds.EROSION_KERNEL_MAX, self.thresholds.EROSION_KERNEL_MAX, on_value_change)
        # cv2.createTrackbar("DILATION ITERATIONS", "Parameters", self.thresholds.DILATION_ITERATIONS_MIN, self.thresholds.DILATION_ITERATIONS_MAX, on_value_change)
        # cv2.createTrackbar("EROSION ITERATIONS", "Parameters", self.thresholds.EROSION_ITERATIONS_MIN, self.thresholds.EROSION_ITERATIONS_MAX, on_value_change)
        # cv2.createTrackbar("WIDTH MIN", "Parameters", self.thresholds.WIDTH_MIN, self.thresholds.WIDTH_MAX, on_value_change)
        # cv2.createTrackbar("WIDTH MAX", "Parameters", self.thresholds.WIDTH_MAX, self.thresholds.WIDTH_MAX, on_value_change)
        # cv2.createTrackbar("HEIGHT MIN", "Parameters", self.thresholds.HEIGHT_MIN, self.thresholds.HEIGHT_MAX, on_value_change)
        # cv2.createTrackbar("HEIGHT MAX", "Parameters", self.thresholds.HEIGHT_MAX, self.thresholds.HEIGHT_MAX, on_value_change)
        
        
        
  

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
            self.thresholds.HUE_MIN = cv2.getTrackbarPos("HUE MIN", "Parameters")
            self.thresholds.SAT_MIN = cv2.getTrackbarPos("SAT MIN", "Parameters")
            self.thresholds.VALUE_MIN = cv2.getTrackbarPos("VALUE MIN", "Parameters")
            self.thresholds.HUE_MAX = cv2.getTrackbarPos("HUE MAX", "Parameters")
            self.thresholds.SAT_MAX = cv2.getTrackbarPos("SAT MAX", "Parameters")
            self.thresholds.VALUE_MAX = cv2.getTrackbarPos("VALUE MAX", "Parameters")         
            # self.thresholds.EDGE_THRESHOLD1 = cv2.getTrackbarPos("EDGE THRESHOLD 1", "Parameters")
            # self.thresholds.EDGE_THRESHOLD2 = cv2.getTrackbarPos("EDGE THRESHOLD 2", "Parameters")
            # self.thresholds.CORNER_POINTS_MIN = cv2.getTrackbarPos("CORNERS MIN", "Parameters")
            # self.thresholds.CORNER_POINTS_MAX = cv2.getTrackbarPos("CORNERS MAX", "Parameters")
            self.thresholds.AREA_MIN = cv2.getTrackbarPos("AREA MIN", "Parameters")
            self.thresholds.AREA_MAX = cv2.getTrackbarPos("AREA MAX", "Parameters")
            # self.thresholds.EROSION_ITERATIONS_MIN = cv2.getTrackbarPos("EROSION ITERATIONS", "Parameters")
            # self.thresholds.DILATION_ITERATIONS_MIN = cv2.getTrackbarPos("DILATION ITERATIONS", "Parameters")
            # self.thresholds.DILATION_KERNEL_MIN = cv2.getTrackbarPos("DILATION KERNEL MIN", "Parameters")
            # self.thresholds.DILATION_KERNEL_MAX = cv2.getTrackbarPos("DILATION KERNEL MAX", "Parameters")
            # self.thresholds.EROSION_KERNEL_MIN = cv2.getTrackbarPos("EROSION KERNEL MIN", "Parameters")
            # self.thresholds.EROSION_KERNEL_MAX = cv2.getTrackbarPos("EROSION KERNEL MAX", "Parameters")
            # self.thresholds.WIDTH_MIN = cv2.getTrackbarPos("WIDTH MIN", "Parameters")
            # self.thresholds.WIDTH_MAX = cv2.getTrackbarPos("WIDTH MAX", "Parameters")
            # self.thresholds.HEIGHT_MIN = cv2.getTrackbarPos("HEIGHT MIN", "Parameters")
            # self.thresholds.HEIGHT_MAX = cv2.getTrackbarPos("HEIGHT MAX", "Parameters")


            self.colours = {((self.thresholds.HUE_MIN,self.thresholds.SAT_MIN,self.thresholds.VALUE_MIN), 
            (self.thresholds.HUE_MAX,self.thresholds.SAT_MAX,self.thresholds.VALUE_MAX)) : ""} # Default value  


               
             

        if(self.colours):
            hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)

            colour_space = hsv

           


            masks = []
            mask = cv2.inRange(colour_space, np.array(list(self.colours.items())[0][0][0]), 
            np.array((list(self.colours.items())[0][0][1]))) # First Mask
            

            colour_detected_capture = None
            # Establish The Individual Masks
           
            for colour in self.colours:
                masks.append((cv2.inRange(colour_space, np.array(colour[0]), np.array(colour[1])), self.colours[colour]))

            for mask in range(len(masks)):
                kernel = np.ones((self.thresholds.DILATION_KERNEL_MIN, self.thresholds.DILATION_KERNEL_MAX), np.uint8)
                dilated_mask = cv2.dilate(masks[mask][0], kernel, self.thresholds.DILATION_ITERATIONS_MIN)
                edge_detect = cv2.Canny(dilated_mask, self.thresholds.EDGE_THRESHOLD1, self.thresholds.EDGE_THRESHOLD2, None, 3)
                contours = cv2.findContours(edge_detect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                conts = imutils.grab_contours(contours)
                max_bbox = 0

                for c in conts:
                    perimeter = cv2.arcLength(c,True)
                    approx = cv2.approxPolyDP(c, 0.02*perimeter, True) # Corner points
                    bbox = cv2.boundingRect(approx)
                    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                    bbox_pts = np.float32([[x,y], [x+w, y+h], [x+w, y], [x, y+h]]) # TL = x,y, TR = x+w, y, BL = x,y+h, BR = x+w, y+h

                    center = (int(x+w/2),int(y+h/2)) # Center of bbox
                    
                    # Reduce the detection so only a set size of objects can be detected
                    
                    # if(h > max_bbox):
                    # if(w > self.thresholds.WIDTH_MIN and w < self.thresholds.WIDTH_MAX and h > self.thresholds.HEIGHT_MIN and h < self.thresholds.HEIGHT_MAX):
                    #     if(len(approx) > self.thresholds.CORNER_POINTS_MIN and len(approx) < self.thresholds.CORNER_POINTS_MAX):
                    if(cv2.contourArea(c) > self.thresholds.AREA_MIN and cv2.contourArea(c) < self.thresholds.AREA_MAX):
                        colour = masks[mask][1]
                        bbox_corner_pts = ((x,y), ((x+w), (y+h)))
                        self.object_handler.add_corner_data(len(approx))
                        self.object_handler.add_coordinates_data((bbox_corner_pts[0][0], bbox_corner_pts[0][1], w, h))
                        self.object_handler.add_boundaries()
                        self.object_handler.add_colour_data(colour)
                        self.object_handler.add_object_to_list()
                        max_bbox = h
            
                


            # Combine the masks into one colour mask
            for colour in range(len(masks)):
                mask = mask + masks[colour][0]
            colour_detected_capture = cv2.bitwise_and(capture, capture, mask = mask)
                
            if(self.use_trackbars):
                cv2.imshow("COLOUR DETECTOR", colour_detected_capture)


        else:
            print("No Colours To Detect!")
            exit()

