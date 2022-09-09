import cv2
from stream_types import Stream_Types
import numpy as np
class Stream_Settings():

    def __init__(self):
        self.stream_cap = None
        self.original_cap = None
        self.path = None
        self.stream_type = None
        self.vision_modes = []
        self.cameraID = 0
        self.is_active = False
        self.use_trackbars = False
        self.thresholds = [[0,0,0],[100,100]] # H,S,V,[Edge thresholds]


    def set_hue(self, new_hue_val):
        self.thresholds[0][0] = new_hue_val

    def set_saturation(self, new_saturation_val):
        self.thresholds[0][1] = new_saturation_val

    def set_brightness(self, new_brightness_val):
        self.thresholds[0][2] = new_brightness_val

    def get_hue(self):
        return self.thresholds[0][0]

    def get_saturation(self):
        return self.thresholds[0][1]

    def get_brightness(self):
        return self.thresholds[0][2]


    def set_edge_threshold_1(self, new_threshold):
        self.thresholds[1][0] = new_threshold

    def set_edge_threshold_2(self, new_threshold):
        self.thresholds[1][1] = new_threshold

    def get_edge_threshold_1(self):
        return self.thresholds[1][0]

    def get_edge_threshold_2(self):
        return self.thresholds[1][1]




    
    def on_value_change(self, val):
            pass

    def add_trackbars(self):
        self.use_trackbars = True
        self.vision_modes.insert(0, self.trackbars)
    
    def trackbars(self):
        if(self.is_active == False):
            self.is_active = True
            cv2.namedWindow("Parameters")
            cv2.resizeWindow("Parameters", 640, 240)
            cv2.createTrackbar("Edge_Threshold1", "Parameters", 150, 255, self.on_value_change)
            cv2.createTrackbar("Edge_Threshold2", "Parameters", 255,255, self.on_value_change)     


    def add_type(self, new_type):
        self.stream_type = new_type


    def add_image_path(self, path):
        self.path = path

    
    def add_camera(self, cameraID):
        self.cameraID = cameraID

         
    def edge_detection(self):
        self.vision_modes.append(self.edge_detector)


    def edge_detector(self):
        if(self.is_active == True):
            self.thresholds[1][0] = cv2.getTrackbarPos("Edge_Threshold1", "Parameters") 
            self.thresholds[1][1] = cv2.getTrackbarPos("Edge_Threshold2", "Parameters")            
        self.stream_cap = cv2.Canny(self.stream_cap, self.thresholds[1][0], self.thresholds[1][1])

    def colour_detection(self):
        self.vision_modes.append(self.colour_detector)


    def colour_detector(self):
        self.stream_cap = self.change_colour()
        self.stream_cap = self.blur()


    def change_colour(self):
        return cv2.cvtColor(self.stream_cap, cv2.COLOR_BGR2GRAY)

    def blur(self):
        return cv2.GaussianBlur(self.stream_cap, (7,7), 1)


    def dilation(self):
        self.vision_modes.append(self.dilator)

    def dilator(self):
        kernel = np.ones((5,5)) # thickness
        return cv2.dilate(self.stream_cap, kernel, iterations=1)




    def erosion(self):
        self.vision_modes.append(self.eroder)

    def eroder(self):
        return

    def contours(self):
        self.vision_modes.append(self.contour_detector)

    def contour_detector(self):
        contours, hierarchy = cv2.findContours(self.stream_cap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return cv2.drawContours(self.stream_cap, self.original_cap, -1, (255,0,255), 7) # colour of contours, width of contours

    def run_vision_modes(self):
        for modes in self.vision_modes:
            modes()
