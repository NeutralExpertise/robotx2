from ctypes import resize
import cv2
from stream_types import Stream_Types
import numpy as np
from thresholds import Thresholds
import keyboard
from screeninfo import get_monitors
class Stream_Settings():

    def __init__(self):
        self.original_cap = None
        self.stream_cap = None
        self.path = None
        self.stream_type = None
        self.vision_modes = []
        self.cameraID = 0
        self.use_trackbars = False
        self.is_active = False
        self.tracker = None
        self.resolution = {"top": get_monitors()[0].y, "left":get_monitors()[0].x, "height": get_monitors()[0].height, "width":get_monitors()[0].width}


    def set_stream_cap(self,new_cap):
        self.stream_cap = new_cap


    
    def on_value_change(self, val):
            pass

    def add_trackbars(self):
        self.use_trackbars = True
        self.vision_modes.insert(0, self.__trackbars)

    def stop_stream(self):
        cv2.destroyAllWindows()
    
    def __trackbars(self):
        if(self.is_active == False):
            self.is_active = True
            cv2.namedWindow("Parameters")
            cv2.resizeWindow("Parameters", 1500, 1000)
            cv2.createTrackbar("Edge Threshold1", "Parameters", Thresholds.EDGE_THRESHOLD1, Thresholds.EDGE_THRESHOLD2, self.on_value_change) # 255
            cv2.createTrackbar("Edge Threshold2", "Parameters", Thresholds.EDGE_THRESHOLD2, Thresholds.EDGE_THRESHOLD2, self.on_value_change) # 139

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

            
            cv2.createTrackbar("SIZE WIDTH", "Parameters", self.resolution["width"], self.resolution["width"], self.on_value_change) 
            cv2.createTrackbar("SIZE HEIGHT", "Parameters", self.resolution["height"], self.resolution["height"], self.on_value_change) 
            



            # cv2.createTrackbar("DILATION KERNEL", "Parameters", Thresholds.DILATION_KERNEL, Thresholds.DILATION_KERNEL_MAX, self.on_value_change)
            # cv2.createTrackbar("DILATION KERNEL MAX", "Parameters", Thresholds.DILATION_KERNEL_MAX, Thresholds.DILATION_KERNEL_MAX, self.on_value_change)
            # cv2.createTrackbar("EROSION KERNEL", "Parameters", Thresholds.EROSION_KERNEL, Thresholds.EROSION_KERNEL_MAX, self.on_value_change)
            # cv2.createTrackbar("EROSION KERNEL MAX", "Parameters", Thresholds.EROSION_KERNEL_MAX, Thresholds.EROSION_KERNEL_MAX, self.on_value_change)

            # cv2.createTrackbar("BLUR KERNEL", "Parameters", Thresholds.BLUR_KERNEL, Thresholds.BLUR_KERNEL_MAX, self.on_value_change)
            # cv2.createTrackbar("BLUR KERNEL MAX", "Parameters", Thresholds.BLUR_KERNEL_MAX, Thresholds.BLUR_KERNEL_MAX, self.on_value_change)





    def add_type(self, new_type):
        self.stream_type = new_type


    def add_image_path(self, path):
        self.path = path

    
    def add_camera(self, cameraID):
        self.cameraID = cameraID



    def object_tracking(self):
        self.tracker = cv2.legacy.TrackerCSRT_create() # Most accurate tracker
        # self.vision_modes.append(self.__object_tracker)
        


    def __object_tracker(self):
        if(self.is_active == False):
            # Initialise the tracker
            bbox = cv2.selectROI("Tracking", self.stream_cap, False)
            self.tracker.init(self.stream_cap, bbox)
            self.is_active = True

        timer = cv2.getTickCount()
        success,bbox = self.tracker.update(self.stream_cap)
        if(success):
            x,y,w,h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            cv2.rectangle(self.stream_cap, (x,y), ((x+w), (y+h)), (255,0,255),3,1)
            cv2.putText(self.stream_cap, "TRACKING", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        else:
            cv2.putText(self.stream_cap, "TRACKING LOST", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
        cv2.putText(self.stream_cap, str(int(fps)), (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        cv2.imshow("TRACKER", self.stream_cap)
            

    def resize(self):
        self.vision_modes.append(self.__resizer)

    def __resizer(self):
        self.stream_cap = cv2.resize(self.stream_cap, (cv2.getTrackbarPos("SIZE WIDTH", "Parameters"), cv2.getTrackbarPos("SIZE HEIGHT", "Parameters")))
        cv2.imshow("Resized", self.stream_cap)




         
    def edge_detection(self):
        self.vision_modes.append(self.__edge_detector)

    
    def __edge_detector(self):
        imgGrey = cv2.cvtColor(self.stream_cap, cv2.COLOR_BGR2GRAY)
        imgBlur = self.blur(imgGrey)
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

        self.stream_cap = cv2.cvtColor(self.stream_cap, cv2.COLOR_BGR2HSV)
        # # Automatically Detect the colour
        # if(self.use_trackbars == False):
        height, width, _ = self.stream_cap.shape
        cx = int(width/2)
        cy = int(height/2)

        pixel = self.stream_cap[cy, cx]
        Thresholds.HUE_MIN = int(pixel[0])
        Thresholds.SAT_MIN = int(pixel[1])
        Thresholds.VALUE_MIN = int(pixel[2])
        Thresholds.COLOUR = ""
        if Thresholds.HUE_MIN >= Thresholds.RED_HUE and Thresholds.VALUE_MIN < Thresholds.RED_VAL:
            Thresholds.COLOUR = "RED"         
        elif Thresholds.HUE_MIN < Thresholds.ORANGE_HUE and Thresholds.VALUE_MIN < Thresholds.ORANGE_VAL:
            Thresholds.COLOUR = "ORANGE"
        elif Thresholds.HUE_MIN < Thresholds.YELLOW_HUE and Thresholds.VALUE_MIN < Thresholds.YELLOW_VAL:
            Thresholds.COLOUR = "YELLOW"
        elif Thresholds.HUE_MIN < Thresholds.GREEN_HUE and Thresholds.VALUE_MIN < Thresholds.GREEN_VAL:
            Thresholds.COLOUR = "GREEN"
        elif Thresholds.HUE_MIN < Thresholds.BLACK_HUE and Thresholds.VALUE_MIN < Thresholds.BLACK_SAT and Thresholds.SAT_MIN < Thresholds.BLACK_SAT:
            Thresholds.COLOUR = "BLACK"
        elif Thresholds.HUE_MIN <= Thresholds.WHITE_HUE and Thresholds.SAT_MIN < Thresholds.WHITE_SAT: 
            Thresholds.COLOUR = "WHITE"
        elif Thresholds.HUE_MIN < Thresholds.BLUE_HUE and Thresholds.VALUE_MIN < Thresholds.BLUE_VAL: 
            Thresholds.COLOUR = "BLUE"
        elif Thresholds.HUE_MIN < Thresholds.PURPLE_HUE and Thresholds.VALUE_MIN < Thresholds.PURPLE_VAL:
            Thresholds.COLOUR = "PURPLE"

        


        b, g, r = int(pixel[0]), int(pixel[1]), int(pixel[2])

        cv2.putText(self.stream_cap, Thresholds.COLOUR, (10, 70), 0, 1.5, (b, g, r), 3)
        cv2.putText(self.stream_cap, str(b) + " " + str(g) + " " + str(r), (20, 100), 0, 1, (b, g, r), 3)
        cv2.circle(self.stream_cap, (cx, cy), 5, (255, 0, 0), 3) # Focus point
        
        if(self.use_trackbars):
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
        # self.stream_cap = cv2.bitwise_and(self.stream_cap, self.stream_cap, mask = mask)
        # if(self.use_trackbars):
        self.stream_cap = cv2.cvtColor(self.stream_cap, cv2.COLOR_HSV2BGR)
        cv2.imshow("Colour Detector", self.stream_cap)        

    
    def blur(self, img):
        return cv2.GaussianBlur(img, (Thresholds.BLUR_KERNEL,Thresholds.BLUR_KERNEL_MAX), 1)


    def dilate(self, img):
        kernel = np.ones((Thresholds.DILATION_KERNEL,Thresholds.DILATION_KERNEL_MAX)) # thickness
        if(self.use_trackbars):
            Thresholds.DILATION = cv2.getTrackbarPos("DILATION", "Parameters")
        return cv2.dilate(img, kernel, iterations=Thresholds.DILATION)


    def erode(self, img):
        kernel = np.ones((Thresholds.EROSION_KERNEL,Thresholds.EROSION_KERNEL_MAX))
        if(self.use_trackbars):
            Thresholds.EROSION = cv2.getTrackbarPos("EROSION", "Parameters")
        return cv2.dilate(img, kernel, iterations=Thresholds.EROSION)

       
   # Would like to get the right COLOUR contours at some point
    def contour_detector(self, img, modified_img):
        contours, hierarchy = cv2.findContours(modified_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if(self.use_trackbars):
            Thresholds.AREA_MIN = cv2.getTrackbarPos("AREA MIN", "Parameters")
            Thresholds.AREA_MAX = cv2.getTrackbarPos("AREA MAX", "Parameters")
            Thresholds.SHAPE_POINTS = cv2.getTrackbarPos("SHAPE POINTS", "Parameters")
        colour = (Thresholds.HUE_MIN, Thresholds.SAT_MIN, Thresholds.VALUE_MIN)
        for contour in contours:
            area = cv2.contourArea(contour)
            if(area > Thresholds.AREA_MIN and area < Thresholds.AREA_MAX):
                # cv2.drawContours(img, contour, -1, colour, 7)
                perimeter = cv2.arcLength(contour,True)
                approx = cv2.approxPolyDP(contour, 0.02*perimeter, True) # Corner points
                bbox = cv2.boundingRect(approx)
                x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

                
                cv2.rectangle(img, (x,y), ((x+w), (y+h)), colour,3,1)               
                cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, colour, 2)
                cv2.putText(img, "Height: " + str(int(h)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, colour, 2)
                cv2.putText(img, "Width: " + str(int(w)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, colour, 2)
        
              

    def run_vision_modes(self):
        for modes in self.vision_modes:
            modes()
