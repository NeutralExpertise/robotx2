import cv2
from stream_types import Stream_Types
import numpy as np
from thresholds import Thresholds
class Stream_Settings():

    def __init__(self):
        self.original_cap = None
        self.stream_cap = None
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


    def set_stream_cap(self,new_cap):
        self.stream_cap = new_cap


    
    def on_value_change(self, val):
            pass

    def add_trackbars(self):
        self.use_trackbars = True
        self.vision_modes.insert(0, self.__trackbars)
    
    def __trackbars(self):
        if(self.is_active == False):
            self.is_active = True
            cv2.namedWindow("Parameters")
            cv2.resizeWindow("Parameters", 1500, 1000)
            cv2.createTrackbar("Edge Threshold1", "Parameters", Thresholds.EDGE_THRESHOLD1, Thresholds.EDGE_THRESHOLD2, self.on_value_change) # 255
            cv2.createTrackbar("Edge Threshold2", "Parameters", Thresholds.EDGE_THRESHOLD2, Thresholds.EDGE_THRESHOLD2, self.on_value_change) # 139

            cv2.createTrackbar("HUE MIN", "Parameters", Thresholds.HUE_MIN, Thresholds.HUE_MAX, self.on_value_change)
            cv2.createTrackbar("HUE MAX", "Parameters", Thresholds.HUE_MAX, Thresholds.HUE_MAX,self.on_value_change)
            cv2.createTrackbar("SAT MIN", "Parameters", Thresholds.SAT_MIN,Thresholds.SAT_MAX,self.on_value_change)
            cv2.createTrackbar("SAT MAX", "Parameters", Thresholds.SAT_MAX,Thresholds.SAT_MAX,self.on_value_change)
            cv2.createTrackbar("VALUE MIN", "Parameters", Thresholds.VALUE_MIN,Thresholds.VALUE_MAX,self.on_value_change)
            cv2.createTrackbar("VALUE MAX", "Parameters", Thresholds.VALUE_MAX,Thresholds.VALUE_MAX,self.on_value_change)

            # cv2.createTrackbar("AREA MIN", "Parameters", 0,20000, self.on_value_change) 

            cv2.createTrackbar("DILATION", "Parameters", Thresholds.DILATION, Thresholds.DILATION_MAX, self.on_value_change)
            cv2.createTrackbar("EROSION", "Parameters", Thresholds.EROSION, Thresholds.EROSION_MAX, self.on_value_change)

            # cv2.createTrackbar("DILATION KERNEL MIN", "Parameters", 0, 100, self.on_value_change)
            # cv2.createTrackbar("DILATION KERNEL MAX", "Parameters", 0, 100, self.on_value_change)
            # cv2.createTrackbar("EROSION KERNEL MIN", "Parameters", 0, 100, self.on_value_change)
            # cv2.createTrackbar("EROSION KERNEL MAX", "Parameters", 0, 100, self.on_value_change)

            # cv2.createTrackbar("BLUR KERNEL MAX", "Parameters", 0, 100, self.on_value_change)
            # cv2.createTrackbar("BLUR KERNEL MIN", "Parameters", 0, 100, self.on_value_change)

            # cv2.createTrackbar("STREAM Y", "Parameters", mon_resolution["height"]-1, mon_resolution["height"]-1, on_value_change) 
            # cv2.createTrackbar("STREAM X", "Parameters", mon_resolution["width"]-1, mon_resolution["width"]-1, on_value_change)

            # cv2.createTrackbar("SIZE WIDTH", "Parameters", mon_resolution["width"], mon_resolution["width"], on_value_change) 
            # cv2.createTrackbar("SIZE HEIGHT", "Parameters", mon_resolution["height"], mon_resolution["height"], on_value_change)      


    def add_type(self, new_type):
        self.stream_type = new_type


    def add_image_path(self, path):
        self.path = path

    
    def add_camera(self, cameraID):
        self.cameraID = cameraID

         
    def edge_detection(self):
        self.vision_modes.append(self.__edge_detector)

    
    def __edge_detector(self):
        imgColour = cv2.cvtColor(self.stream_cap, cv2.COLOR_BGR2GRAY)
        imgBlur = self.blur(imgColour)
        if(self.is_active == True):
            Thresholds.EDGE_THRESHOLD1 = cv2.getTrackbarPos("Edge Threshold1", "Parameters") 
            Thresholds.EDGE_THRESHOLD2 = cv2.getTrackbarPos("Edge Threshold2", "Parameters")            
        imgEdge = cv2.Canny(imgBlur, Thresholds.EDGE_THRESHOLD1, Thresholds.EDGE_THRESHOLD2)
        imgDilate = self.dilate(imgEdge)
        self.stream_cap = self.erode(imgDilate)
        self.contour_detector(self.original_cap, self.stream_cap)
        cv2.imshow("Edge Detector", self.stream_cap)
        

    def colour_detection(self):
        self.vision_modes.append(self.__colour_detector)

    
    def __colour_detector(self):
        # imgHSV = cv2.cvtColor(self.stream_cap, cv2.COLOR_BGR2RGB)
        Thresholds.HUE_MIN = cv2.getTrackbarPos("HUE MIN", "Parameters") 
        Thresholds.HUE_MAX = cv2.getTrackbarPos("HUE MAX", "Parameters") 
        Thresholds.SAT_MIN = cv2.getTrackbarPos("SAT MIN", "Parameters") 
        Thresholds.SAT_MAX = cv2.getTrackbarPos("SAT MAX", "Parameters") 
        Thresholds.VALUE_MIN = cv2.getTrackbarPos("VALUE MIN", "Parameters") 
        Thresholds.VALUE_MAX = cv2.getTrackbarPos("VALUE MAX", "Parameters")
        lower = np.array([Thresholds.HUE_MIN, Thresholds.SAT_MIN, Thresholds.VALUE_MIN])
        upper = np.array([Thresholds.HUE_MAX, Thresholds.SAT_MAX, Thresholds.VALUE_MAX])
        mask = cv2.inRange(self.stream_cap, lower, upper)
        cv2.imshow("MASK", mask)
        self.stream_cap = cv2.bitwise_and(self.stream_cap, self.stream_cap, mask = mask)
        cv2.imshow("Edge Detector", self.stream_cap)
        

    
    def blur(self, img):
        return cv2.GaussianBlur(img, (5,5), 1)


    def dilate(self, img):
        kernel = np.ones((5,5)) # thickness
        Thresholds.DILATION = cv2.getTrackbarPos("DILATION", "Parameters")
        return cv2.dilate(img, kernel, iterations=Thresholds.DILATION)


    def erode(self, img):
        kernel = np.ones((5,5))
        Thresholds.EROSION = cv2.getTrackbarPos("EROSION", "Parameters")
        return cv2.dilate(img, kernel, iterations=Thresholds.EROSION)
        
   
    def contour_detector(self, img, modified_img):
        contours, hierarchy = cv2.findContours(modified_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            area = cv2.contourArea(contour)
            cv2.drawContours(img, contour, -1, (Thresholds.HUE_MIN, Thresholds.SAT_MIN, Thresholds.VALUE_MIN), 7)
            perimeter = cv2.arcLength(contour,True)
            approx = cv2.approxPolyDP(contour, 0.02*perimeter, True) # Corner points
            x,y,w,h = cv2.boundingRect(approx)
            # RGB VALUES
            if(len(approx) == 6):
                cv2.rectangle(img, (x, y), (x + w, y + h), (Thresholds.HUE_MIN, Thresholds.SAT_MIN, Thresholds.VALUE_MIN), 5)
                cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (Thresholds.HUE_MIN, Thresholds.SAT_MIN, Thresholds.VALUE_MIN), 2)
                cv2.putText(img, "Height: " + str(int(h)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (Thresholds.HUE_MIN, Thresholds.SAT_MIN, Thresholds.VALUE_MIN), 2)
                cv2.putText(img, "Width: " + str(int(w)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (Thresholds.HUE_MIN, Thresholds.SAT_MIN, Thresholds.VALUE_MIN), 2)
        

    def run_vision_modes(self):
        for modes in self.vision_modes:
            modes()
