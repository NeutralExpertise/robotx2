from ctypes import resize
import cv2
from stream_types import Stream_Types
from thresholds import Thresholds
import numpy as np
import imutils
class Stream_Settings():

    def __init__(self):
        self.capture = None
        self.modified_capture = None
        self.path = None
        self.stream_type = Stream_Types.CAMERA
        self.vision_modes = []
        self.cameraID = 0
        self.use_trackbars = False
        self.is_active = False
        self.tracking = False
        self.tracker = None




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


    '''FOR TESTING PURPOSES ONLY'''
    def on_value_change(self, val):
        pass

    
    def display_focal_point(self):
            cv2.circle(self.capture, (self.get_focal_point_coords()), 10, (0,255,0), 2)

    def get_focal_point_coords(self):
            height, width, _ = self.capture.shape
            cx = int(width/2)
            cy = int(height/2)
            focal_point = (cx,cy)
            return focal_point

    
    def set_capture_type(self, new_capture):
        self.capture = new_capture

    def set_stream_type(self, new_type):
        self.stream_type = new_type

    def set_image_path(self, path):
        self.path = path

    
    def set_camera(self, cameraID):
        self.cameraID = cameraID



    def resize(self):
        if(self.is_active == False):
            self.vision_modes.append(self.resize)
        else:
            if(self.use_trackbars):
                Thresholds.RESOLUTION_WIDTH, Thresholds.RESOLUTION_HEIGHT = cv2.getTrackbarPos("SIZE WIDTH", "Parameters"), cv2.getTrackbarPos("SIZE HEIGHT", "Parameters")
            # WIDTH, HEIGHT CANNOT BE 0 - IMPOSSIBLE
            if(Thresholds.RESOLUTION_WIDTH == 0):
                Thresholds.RESOLUTION_WIDTH = 1
            if(Thresholds.RESOLUTION_HEIGHT == 0):
                Thresholds.RESOLUTION_HEIGHT = 1    
            self.capture = cv2.resize(self.capture, (Thresholds.RESOLUTION_WIDTH, Thresholds.RESOLUTION_HEIGHT))



    def colour_detection(self):
        if(self.is_active == False):
            self.vision_modes.append(self.colour_detection)
        else:
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



    def object_tracker(self, tracker="CSRT"):
        if(tracker.upper() == "BOOSTING"):
            self.tracker = cv2.legacy.TrackerBoosting_create()
        elif(tracker.upper() == "MIL"):
            self.tracker = cv2.legacy.TrackerMIL_create()
        elif(tracker.upper() == "KCF"): 
            self.tracker = cv2.legacy.TrackerKCF_create()
        elif(tracker.upper() == "TLD"):
            self.tracker = cv2.legacy.TrackerTLD_create()
        elif(tracker.upper() == "MEDIANFLOW"):
            self.tracker = cv2.legacy.TrackerMedianFlow_create()
        elif(tracker.upper() == "MOSSE"):
            self.tracker = cv2.legacy.TrackerMOSSE_create() # Did not even detect still image objects
        elif(tracker.upper() == "CSRT"):
            self.tracker = cv2.legacy.TrackerCSRT_create() # Did not even detect still image objects


    def initialse_tracker(self, object):
        self.tracker.init(self.capture, object)
        self.tracking = True

    def update_tracker(self, object):
        if(self.tracker != None):
                success, tracked_obj = self.tracker.update(self.capture)
                if(success):
                    cv2.putText(self.capture, "TRACKING ", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                    cv2.rectangle(self.capture, (object[0][0],object[0][1]), ((object[1][0]), (object[1][1])), (255,0,255),3,1)
                else:
                    cv2.putText(self.capture, "TRACKING LOST", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)





    def edge_detection(self):
        if(self.is_active == False):
            self.vision_modes.append(self.edge_detection)
        else:
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
        bboxes = set([])
        conts = cv2.findContours(self.modified_capture, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        conts = imutils.grab_contours(conts)
        conts_img = np.zeros(self.capture.shape)
        conts_img = cv2.drawContours(conts_img, conts, -1, (0,255,0), 2)
        if(self.use_trackbars):
            Thresholds.AREA_MIN = cv2.getTrackbarPos("AREA MIN", "Parameters")
            Thresholds.AREA_MAX = cv2.getTrackbarPos("AREA MAX", "Parameters")
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
                if(len(approx) == 8):
                    cv2.drawContours(conts_img, [c], -1, (0,255,0), 2)
                    if(h > max_bbox):
                        bbox_coords = ((x,y), ((x+w), (y+h)))
                        if(self.tracker != None):
                        # Initialise to track the first object detected
                            if(self.tracking == False):
                                self.initialse_tracker(bbox)
                            else:
                                self.update_tracker(bbox_coords)

                        
                        # self.set_boundaries(bbox_coords)
                            
                        max_bbox = h
                        
                        # cv2.rectangle(self.capture, (bbox_coords[0][0], bbox_coords[0][1]), (bbox_coords[1][0], bbox_coords[1][1]), (255,255,255),3,1)
                        bboxes.add(bbox)
                        cv2.line(self.capture, (center), (self.get_focal_point_coords()), (255,0,255), 2)
                        # cv2.putText(self.original_cap, self.calculate_distance((x,y), self.focal_point), (center), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0), 2)
                        cv2.putText(conts_img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                        cv2.putText(conts_img, "Height: " + str(int(h)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                        cv2.putText(conts_img, "Width: " + str(int(w)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                        cv2.putText(conts_img, "x: " + str(x), (x + w + 20, y + 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                        cv2.putText(conts_img, "y: " + str(y), (x + w + 20, y + 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
            if(self.use_trackbars):
                cv2.imshow("CONTOURS", conts_img)






    def set_boundaries(self, objects):
        # bbox_list = list(sorted(objects))

        #     # Object Avoidance Boundaries
        # for bbox in range(len(bbox_list)):
        #     x, y, w, h = int(bbox_list[bbox][0]), int(bbox_list[bbox][1]), int(bbox_list[bbox][2]), int(bbox_list[bbox][3])
                cv2.rectangle(self.capture, (objects[0][0]-100, objects[0][1]-100), ((objects[1][0])+100, (objects[1][1])+100), (85,51,255),10,1)










    



        


    