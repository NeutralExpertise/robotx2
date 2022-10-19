import cv2
from object import Object
from stream_settings import Stream_Settings
from thresholds import Thresholds
import numpy as np
import imutils
class Object_Detector(Stream_Settings):
    objects = set([])
    

    def __init__(self):
        self.use_trackbars = False
        self.tracking = False
        self.tracker = None
        self.track_objects = False


    def get_objects(self):
        return self.objects


    def get_object(self, index):
        try:
            object = self.objects[index]
            return object
        except IndexError:
            print("Index Out Of Range")   


    def add_object(self, object):
        # Add the object
        self.objects.add(object)


    '''FOR TESTING PURPOSES ONLY'''
    def add_trackbars(self):
        self.use_trackbars = True
        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 1500, 1000)
        cv2.createTrackbar("EDGE THRESHOLD1", "Parameters", Thresholds.EDGE_THRESHOLD1, Thresholds.EDGE_THRESHOLD2, self.on_value_change) # 255
        cv2.createTrackbar("EDGE THRESHOLD2", "Parameters", Thresholds.EDGE_THRESHOLD2, Thresholds.EDGE_THRESHOLD2, self.on_value_change) # 139

        cv2.createTrackbar("SHAPE POINTS", "Parameters", Thresholds.SHAPE_POINTS, Thresholds.SHAPE_POINTS_MAX, self.on_value_change)

        cv2.createTrackbar("HUE MIN", "Parameters", Thresholds.HUE_MIN, Thresholds.HUE_MAX, self.on_value_change)
        cv2.createTrackbar("HUE MAX", "Parameters", Thresholds.HUE_MAX, Thresholds.HUE_MAX,self.on_value_change)
        cv2.createTrackbar("SAT MIN", "Parameters", Thresholds.SAT_MIN,Thresholds.SAT_MAX,self.on_value_change)
        cv2.createTrackbar("SAT MAX", "Parameters", Thresholds.SAT_MAX,Thresholds.SAT_MAX,self.on_value_change)
        cv2.createTrackbar("VALUE MIN", "Parameters", Thresholds.VALUE_MIN,Thresholds.VALUE_MAX,self.on_value_change)
        cv2.createTrackbar("VALUE MAX", "Parameters", Thresholds.VALUE_MAX,Thresholds.VALUE_MAX,self.on_value_change)

        cv2.createTrackbar("AREA MIN", "Parameters", Thresholds.AREA_MIN,Thresholds.AREA_MAX, self.on_value_change)
        cv2.createTrackbar("AREA MAX", "Parameters", Thresholds.AREA_MAX,Thresholds.AREA_MAX, self.on_value_change)
        

        cv2.createTrackbar("DILATION", "Parameters", Thresholds.DILATION, Thresholds.DILATION_MAX, self.on_value_change)
        cv2.createTrackbar("EROSION", "Parameters", Thresholds.EROSION, Thresholds.EROSION_MAX, self.on_value_change)

        
        cv2.createTrackbar("SIZE WIDTH", "Parameters", Thresholds.RESOLUTION_WIDTH, Thresholds.RESOLUTION_WIDTH, self.on_value_change) 
        cv2.createTrackbar("SIZE HEIGHT", "Parameters", Thresholds.RESOLUTION_HEIGHT, Thresholds.RESOLUTION_HEIGHT, self.on_value_change) 

        cv2.createTrackbar("CONTOURS", "Parameters", 0, 100, self.on_value_change)
        cv2.createTrackbar("CORNER POINTS", "Parameters", 0, Thresholds.CORNER_POINTS, self.on_value_change)


    '''FOR TESTING PURPOSES ONLY'''
    def on_value_change(self, val):
        pass

        

    def add_colour_detection(self):
                hsv = cv2.cvtColor(self.capture, cv2.COLOR_BGR2HSV)

                if(self.use_trackbars):
                    # Thresholds.GREEN_LOWER[0] = Thresholds.HUE_MIN = cv2.getTrackbarPos("HUE MIN", "Parameters")
                    # Thresholds.GREEN_LOWER[1] = Thresholds.SAT_MIN = cv2.getTrackbarPos("SAT MIN", "Parameters")
                    # Thresholds.GREEN_LOWER[2] = Thresholds.VALUE_MIN = cv2.getTrackbarPos("VALUE MIN", "Parameters")
                    # Thresholds.GREEN_UPPER[0] = Thresholds.HUE_MAX = cv2.getTrackbarPos("HUE MAX", "Parameters")
                    # Thresholds.GREEN_UPPER[1] = Thresholds.SAT_MAX = cv2.getTrackbarPos("SAT MAX", "Parameters")
                    # Thresholds.GREEN_UPPER[2] = Thresholds.VALUE_MAX = cv2.getTrackbarPos("VALUE MAX", "Parameters")

                    Thresholds.RED_LOWER[0] = Thresholds.HUE_MIN = cv2.getTrackbarPos("HUE MIN", "Parameters")
                    Thresholds.RED_LOWER[1] = Thresholds.SAT_MIN = cv2.getTrackbarPos("SAT MIN", "Parameters")
                    Thresholds.RED_LOWER[2] = Thresholds.VALUE_MIN = cv2.getTrackbarPos("VALUE MIN", "Parameters")
                    Thresholds.RED_UPPER[0] = Thresholds.HUE_MAX = cv2.getTrackbarPos("HUE MAX", "Parameters")
                    Thresholds.RED_UPPER[1] = Thresholds.SAT_MAX = cv2.getTrackbarPos("SAT MAX", "Parameters")
                    Thresholds.RED_UPPER[2] = Thresholds.VALUE_MAX = cv2.getTrackbarPos("VALUE MAX", "Parameters")

                    # Thresholds.WHITE_LOWER[0] = Thresholds.HUE_MIN = cv2.getTrackbarPos("HUE MIN", "Parameters")
                    # Thresholds.WHITE_LOWER[1] = Thresholds.SAT_MIN = cv2.getTrackbarPos("SAT MIN", "Parameters")
                    # Thresholds.WHITE_LOWER[2] = Thresholds.VALUE_MIN = cv2.getTrackbarPos("VALUE MIN", "Parameters")
                    # Thresholds.WHITE_UPPER[0] = Thresholds.HUE_MAX = cv2.getTrackbarPos("HUE MAX", "Parameters")
                    # Thresholds.WHITE_UPPER[1] = Thresholds.SAT_MAX = cv2.getTrackbarPos("SAT MAX", "Parameters")
                    # Thresholds.WHITE_UPPER[2] = Thresholds.VALUE_MAX = cv2.getTrackbarPos("VALUE MAX", "Parameters")

                red_mask = cv2.inRange(hsv, Thresholds.RED_LOWER, Thresholds.RED_UPPER)
                green_mask = cv2.inRange(hsv, Thresholds.GREEN_LOWER, Thresholds.GREEN_UPPER)
                white_mask = cv2.inRange(hsv, Thresholds.WHITE_LOWER, Thresholds.WHITE_UPPER)
                black_mask = cv2.inRange(hsv, Thresholds.BLACK_LOWER, Thresholds.BLACK_UPPER)

                mask = red_mask + green_mask + white_mask + black_mask
            
                mask = red_mask + green_mask

                self.modified_capture = cv2.bitwise_and(self.capture, self.capture, mask = mask) # Merge the original with the mask
                if(self.use_trackbars):
                    cv2.imshow("COLOUR DETECTOR", self.modified_capture)
                    cv2.imshow("MASK", mask)


    def blur(self, capture):
        return cv2.GaussianBlur(capture, (Thresholds.BLUR_KERNEL, Thresholds.BLUR_KERNEL_MAX), 1)


    
    def dilation(self, capture):
        kernel = np.ones((Thresholds.DILATION_KERNEL,Thresholds.DILATION_KERNEL_MAX)) # thickness
        if(self.use_trackbars):
            Thresholds.DILATION = cv2.getTrackbarPos("DILATION", "Parameters")
        return cv2.dilate(capture, kernel, iterations=Thresholds.DILATION)


    def erosion(self, img):
        kernel = np.ones((Thresholds.EROSION_KERNEL,Thresholds.EROSION_KERNEL_MAX))
        if(self.use_trackbars):
            Thresholds.EROSION = cv2.getTrackbarPos("EROSION", "Parameters")
        return cv2.dilate(img, kernel, iterations=Thresholds.EROSION)


    def add_object_tracking(self):
        if(self.tracker != None):
            self.track_objects = True
            self.initialize_tracker()
        else:
            self.update_tracker(self.objects)


    def set_tracker(self, tracker):
        self.tracker = tracker


    def initialize_tracker(self):
        self.tracker = cv2.legacy.MultiTracker.create()

    def update_tracker(self):
            for object in self.objects:
                    self.tracker.add(self.create_tracker(), self.capture, object)
            success, bboxes = self.tracker.update(self.capture)
            if(success):
                cv2.putText(self.capture, "TRACKING ", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                for object in bboxes:
                    pt1 = (int(object[0]), int(object[1]))
                    pt2 = (int(object[0] + object[2]), int(object[1] + object[3]))
                    cv2.rectangle(self.capture, pt1, pt2, (255,0,255),3,1)
                    for object in self.objects:
                        object.check_violations()
                

            else:
                cv2.putText(self.capture, "TRACKING LOST", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            self.check_distance_thresholds()
                    
            
              

    def create_tracker(self, tracker="CSRT"):
        if(tracker.upper() == "BOOSTING"):
            tracker = cv2.legacy.TrackerBoosting_create()
        elif(tracker.upper() == "MIL"):
            tracker = cv2.legacy.TrackerMIL_create()
        elif(tracker.upper() == "KCF"): 
            tracker = cv2.legacy.TrackerKCF_create()
        elif(tracker.upper() == "TLD"):
            tracker = cv2.legacy.TrackerTLD_create()
        elif(tracker.upper() == "MEDIANFLOW"):
            tracker = cv2.legacy.TrackerMedianFlow_create()
        elif(tracker.upper() == "MOSSE"):
            tracker = cv2.legacy.TrackerMOSSE_create() # Did not even detect still image objects
        elif(tracker.upper() == "CSRT"):
            tracker = cv2.legacy.TrackerCSRT_create()
        return tracker


    


    def add_edge_detection(self):
            grey_scale = cv2.cvtColor(self.modified_capture, cv2.COLOR_BGR2GRAY)
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
            self.modified_capture = erode
            self.__contour_detection()
            if(self.use_trackbars):
                cv2.imshow("Edge Detector", self.modified_capture)


    def __contour_detection(self):
        conts = cv2.findContours(self.modified_capture, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        conts = imutils.grab_contours(conts)
        conts_img = np.zeros(self.capture.shape)
        conts_img = cv2.drawContours(conts_img, conts, -1, (0,255,0), 2)
        if(self.use_trackbars):
            Thresholds.AREA_MIN = cv2.getTrackbarPos("AREA MIN", "Parameters")
            Thresholds.AREA_MAX = cv2.getTrackbarPos("AREA MAX", "Parameters")
            Thresholds.CORNER_POINTS = cv2.getTrackbarPos("CORNER POINTS", "Parameters")
            
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
                if(len(approx) == Thresholds.CORNER_POINTS):
                    cv2.drawContours(conts_img, [c], -1, (0,255,0), 2)
                    # Only display a box over the object itself and ignore all the shapes detected INSIDE the object itself
                    if(h > max_bbox):
                        bbox_coords = ((x,y), ((x+w), (y+h)))
                        object = Object()
                        object.set_coordinates(bbox)
                        object.set_num_corners(len(approx))
                        object.plot_data()
                                             
            
                        max_bbox = h
                        

            if(self.use_trackbars):
                cv2.imshow("CONTOURS", conts_img)

    
    def check_distance_thresholds(self):
        if(len(self.objects) == 2):
            objects = list(self.objects)
            if(objects[0].get_distance() != objects[1].get_distance()):
                print("DISTANCE INEQUALITY VIOLATION")
            






                    


    # Check if focal point enter's an object's boundary zone (Means boat is not centered)
    def check_violations(self):
        focal_point = self.get_focal_point_coords()
        for object in self.objects:
            x = object.get_coordinates()[0][0]
            y = object.get_coordinates()[0][1]
            w = object.get_coordinates()[1][0]
            h = object.get_coordinates()[1][1]
            if(self.get_focal_point_coords()[0] >= x and 
            self.get_focal_point_coords()[0] <= w and 
            self.get_focal_point_coords()[1] > y and 
            self.get_focal_point_coords()[1] < h):
                cv2.putText(self.capture, "BOUNDARY VIOLATION ", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 10)
                cv2.putText(self.capture, "BOUNDARY VIOLATION ", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                return True
        else:
            cv2.putText(self.capture, "", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 10)
            cv2.putText(self.capture, "", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        return False






