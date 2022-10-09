import cv2
from cv2 import FILLED
from stream_types import Stream_Types
import numpy as np
from thresholds import Thresholds
import keyboard
from screeninfo import get_monitors
import imutils
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
        self.focal_point = None



    def display_focal_point(self):
        self.vision_modes.append(self.__focal_point)

    def __focal_point(self):
        height, width, _ = self.original_cap.shape
        cx = int(width/2)
        cy = int(height/2)
        self.focal_point = (cx,cy)

        cv2.circle(self.original_cap, (self.focal_point), 10, (0,255,0), 2)



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

            
            cv2.createTrackbar("SIZE WIDTH", "Parameters", self.resolution["width"], self.resolution["width"], self.on_value_change) 
            cv2.createTrackbar("SIZE HEIGHT", "Parameters", self.resolution["height"], self.resolution["height"], self.on_value_change) 

            cv2.createTrackbar("CONTOURS", "Parameters", 0, 100, self.on_value_change) 

            


    


    def add_type(self, new_type):
        self.stream_type = new_type


    def add_image_path(self, path):
        self.path = path

    
    def add_camera(self, cameraID):
        self.cameraID = cameraID



    def object_tracking(self):
        self.tracker = cv2.legacy.TrackerCSRT_create() # Most accurate tracker
        # self.vision_modes.append(self.__object_tracker)
        


    # def __object_tracker(self, ROI):
    #     if(self.is_active == False):
    #         # Initialise the tracker
    #         bbox = cv2.selectROI("Tracking", ROI, False)
    #         self.tracker.init(self.stream_cap, bbox)
    #         self.is_active = True

    #     timer = cv2.getTickCount()
    #     success,bbox = self.tracker.update(self.stream_cap)
    #     if(success):
    #         x,y,w,h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    #         cv2.rectangle(self.stream_cap, (x,y), ((x+w), (y+h)), (255,0,255),3,1)
    #         cv2.putText(self.stream_cap, "TRACKING", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    #     else:
    #         cv2.putText(self.stream_cap, "TRACKING LOST", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    #     fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    #     cv2.putText(self.stream_cap, str(int(fps)), (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    #     cv2.imshow("TRACKER", self.stream_cap)
            

    def resize(self):
        self.vision_modes.append(self.__resizer)

    def __resizer(self):
        self.stream_cap = cv2.resize(self.stream_cap, (cv2.getTrackbarPos("SIZE WIDTH", "Parameters"), cv2.getTrackbarPos("SIZE HEIGHT", "Parameters")))
        cv2.imshow("Resized", self.stream_cap)




         


    def colour_detection(self):
        self.vision_modes.append(self.__colour_detector)

    
    def __colour_detector(self):

            
            hsv = cv2.cvtColor(self.original_cap, cv2.COLOR_BGR2HSV)


            # Thresholds.GREEN_LOWER[0] = Thresholds.HUE_MIN = cv2.getTrackbarPos("HUE MIN", "Parameters")
            # Thresholds.GREEN_LOWER[1] = Thresholds.SAT_MIN = cv2.getTrackbarPos("SAT MIN", "Parameters")
            # Thresholds.GREEN_LOWER[2] = Thresholds.VALUE_MIN = cv2.getTrackbarPos("VALUE MIN", "Parameters")
            # Thresholds.GREEN_UPPER[0] = Thresholds.HUE_MAX = cv2.getTrackbarPos("HUE MAX", "Parameters")
            # Thresholds.GREEN_UPPER[1] = Thresholds.SAT_MAX = cv2.getTrackbarPos("SAT MAX", "Parameters")
            # Thresholds.GREEN_UPPER[2] = Thresholds.VALUE_MAX = cv2.getTrackbarPos("VALUE MAX", "Parameters")

            # Thresholds.RED_LOWER[0] = Thresholds.HUE_MIN = cv2.getTrackbarPos("HUE MIN", "Parameters")
            # Thresholds.RED_LOWER[1] = Thresholds.SAT_MIN = cv2.getTrackbarPos("SAT MIN", "Parameters")
            # Thresholds.RED_LOWER[2] = Thresholds.VALUE_MIN = cv2.getTrackbarPos("VALUE MIN", "Parameters")
            # Thresholds.RED_UPPER[0] = Thresholds.HUE_MAX = cv2.getTrackbarPos("HUE MAX", "Parameters")
            # Thresholds.RED_UPPER[1] = Thresholds.SAT_MAX = cv2.getTrackbarPos("SAT MAX", "Parameters")
            # Thresholds.RED_UPPER[2] = Thresholds.VALUE_MAX = cv2.getTrackbarPos("VALUE MAX", "Parameters")

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
            # mask = white_mask
            mask = red_mask + green_mask

            self.stream_cap = cv2.bitwise_and(self.original_cap, self.original_cap, mask = mask) # Merge the original with the mask

            cv2.imshow("Colour Detector", self.stream_cap)

            cv2.imshow("MASK", mask)
            cv2.imshow("RED MASK", red_mask)
            cv2.imshow("GREEN MASK", green_mask)
            self.stream_cap = cv2.bitwise_and(self.original_cap, self.original_cap, mask = mask) # Merge the original with the mask
            






            
            
            
                            # Adding line between points
                            # self.bboxes.add(bbox)
                            # bbox_list = list(self.bboxes)
                            # other_bbox = 0
                            # for box in range(len(bbox_list)):
                            #     if(bbox_list[box][2]*bbox_list[box][3] < Thresholds.AREA_MIN):
                            #         self.bboxes.remove(bbox_list[box])
                                    
                            #     if(other_bbox != len(bbox_list)):
                            #         center = (int(bbox_list[box][0]+bbox_list[box][2]/2),int(bbox_list[box][1]+bbox_list[box][3]/2))
                            #         other_center = (int(bbox_list[other_bbox][0]+bbox_list[other_bbox][2]/2),int(bbox_list[other_bbox][1]+bbox_list[other_bbox][3]/2))
                            #         cv2.line(self.original_cap, (center), (other_center), (0,255,0), 2)
                            #         line_center = ((center), (other_center))

                            #         line_center = (int(line_center[0][0] + line_center[0][0] / 2), int(line_center[0][1] + line_center[0][1] / 2))
                            #         cv2.circle(self.original_cap, (line_center), 5, (255,255,0), FILLED)
                            #         other_bbox = box+1
                            #     cv2.circle(self.original_cap, (line_center), 5, (255,255,255), FILLED)
                            
                            
                            
                                



                            

                            
                            
       
            

                




            # cv2.imshow("Colour Detector", self.stream_cap)        
            # self.contour_detector(self.original_cap, Thresholds.RED_LOWER, red_mask)
            # self.contour_detector(self.original_cap, Thresholds.GREEN_LOWER, green_mask)
            # self.contour_detector(self.original_cap, Thresholds.WHITE_LOWER, white_mask)
            # self.contour_detector(self.original_cap, Thresholds.BLACK_LOWER, black_mask)
    
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



    def edge_detection(self):
        self.vision_modes.append(self.__edge_detector)

    
    def __edge_detector(self):
        imgGrey = cv2.cvtColor(self.stream_cap, cv2.COLOR_BGR2GRAY)
        imgBlur = self.blur(imgGrey)
        if(self.is_active == True):
            Thresholds.EDGE_THRESHOLD1 = cv2.getTrackbarPos("EDGE THRESHOLD1", "Parameters") 
            Thresholds.EDGE_THRESHOLD2 = cv2.getTrackbarPos("EDGE THRESHOLD2", "Parameters")            
        imgEdge = cv2.Canny(imgBlur, Thresholds.EDGE_THRESHOLD1, Thresholds.EDGE_THRESHOLD2)
        kernel = np.ones((5,5))
        imgDil = cv2.dilate(imgEdge, kernel, iterations=cv2.getTrackbarPos("DILATION", "Parameters"))
        imgThre = cv2.erode(imgDil, kernel, iterations=cv2.getTrackbarPos("EROSION", "Parameters"))
        self.stream_cap = imgThre
        self.contour_detector()
        cv2.imshow("Edge Detector", self.stream_cap)

       
   
    def contour_detector(self):
        bboxes = set([])
        conts = cv2.findContours(self.stream_cap, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        conts = imutils.grab_contours(conts)
        conts_img = np.zeros(self.original_cap.shape)
        conts_img = cv2.drawContours(conts_img, conts, -1, (0,255,0), 2)
        # Thresholds.AREA_MIN = cv2.getTrackbarPos("AREA MIN", "Parameters")
        # Thresholds.AREA_MAX = cv2.getTrackbarPos("AREA MAX", "Parameters")
        max_bbox = 0
        for c in conts:
            perimeter = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c, 0.02*perimeter, True) # Corner points
            bbox = cv2.boundingRect(approx)
            x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            bbox_pts = np.float32([[x,y], [x+w, y+h], [x+w, y], [x, y+h]]) # TL = x,y, TR = x+w, y, BL = x,y+h, BR = x+w, y+h

            center = (int(x+w/2),int(y+h/2))
            
            if(cv2.contourArea(c) > Thresholds.AREA_MIN and cv2.contourArea(c) < Thresholds.AREA_MAX):
                if(len(approx) == 8):
                    cv2.drawContours(conts_img, [c], -1, (0,255,0), 2)
                    if(h > max_bbox):
                        max_bbox = h
                        bbox_coords = ((x,y), ((x+w), (y+h)))
                        cv2.rectangle(self.original_cap, (bbox_coords[0][0], bbox_coords[0][1]), (bbox_coords[1][0], bbox_coords[1][1]), (255,255,255),3,1)
                        bboxes.add(bbox_coords)
                        self.set_boundaries(bboxes)
                        cv2.line(self.original_cap, (center), (self.focal_point), (255,0,255), 2)
                        cv2.putText(conts_img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                        cv2.putText(conts_img, "Height: " + str(int(h)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                        cv2.putText(conts_img, "Width: " + str(int(w)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                        cv2.putText(conts_img, "x: " + str(x), (x + w + 20, y + 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                        cv2.putText(conts_img, "y: " + str(y), (x + w + 20, y + 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
            cv2.imshow("CONTOURS", conts_img)



    def set_boundaries(self, objects):
        bbox_list = list(sorted(objects))
        
        for bbox in range(len(bbox_list)):
            cv2.rectangle(self.original_cap, (bbox_list[bbox][0][0]-100, bbox_list[bbox][0][1]-100), (bbox_list[bbox][1][0]+100, bbox_list[bbox][1][1]+100), (85,51,255),10,1)
            cv2.rectangle(self.original_cap, (bbox_list[bbox][0][0]+200, bbox_list[bbox][0][1]-200), (bbox_list[bbox][1][0]+100, bbox_list[bbox][1][1]+200), (85,51,255),10,1)
            


        # contours = cv2.findContours(modified_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # contours = imutils.grab_contours(contours)
        # colour_rgb = (int(colour[0]), int(colour[1]), int(colour[2]))
        # colour_text = "UNDEFINED"

        # if(colour_rgb[0] >= Thresholds.GREEN_LOWER[0] 
        # and colour_rgb[1] >= Thresholds.GREEN_LOWER[1] 
        # and colour_rgb[2] >= Thresholds.GREEN_LOWER[2] 
        # and colour_rgb[0] <= Thresholds.GREEN_UPPER[0]
        # and colour_rgb[1] <= Thresholds.GREEN_UPPER[1] 
        # and colour_rgb[2] <= Thresholds.GREEN_UPPER[2]):
        #     colour_text = "GREEN"
        #     colour_rgb = (0,255,0)
        # elif(colour_rgb[0] >= Thresholds.RED_LOWER[0] 
        # and colour_rgb[1] >= Thresholds.RED_LOWER[1] 
        # and colour_rgb[2] >= Thresholds.RED_LOWER[2]
        # and colour_rgb[0] <= Thresholds.RED_UPPER[0]
        # and colour_rgb[1] <= Thresholds.RED_UPPER[1] 
        # and colour_rgb[2] <= Thresholds.RED_UPPER[2]):
        #     colour_text = "RED"
        #     colour_rgb = (0,0,255)
        # elif(colour_rgb[0] >= Thresholds.WHITE_LOWER[1] 
        # and colour_rgb[1] >= Thresholds.WHITE_LOWER[1] 
        # and colour_rgb[2] >= Thresholds.WHITE_LOWER[2] 
        # and colour_rgb[0] <= Thresholds.WHITE_UPPER[0]
        # and colour_rgb[1] <= Thresholds.WHITE_UPPER[1] 
        # and colour_rgb[2] <= Thresholds.WHITE_UPPER[2]):
        #     colour_text = "WHITE"
        #     colour_rgb = (255,255,255)
        # elif(colour_rgb[0] >= Thresholds.BLACK_LOWER[0] 
        # and colour_rgb[1] >= Thresholds.BLACK_LOWER[1] 
        # and colour_rgb[2] >= Thresholds.BLACK_LOWER[2] 
        # and colour_rgb[0] <= Thresholds.BLACK_UPPER[0]
        # and colour_rgb[1] <= Thresholds.BLACK_UPPER[1] 
        # and colour_rgb[2] <= Thresholds.BLACK_UPPER[2]):
        #     colour_text = "BLACK"
        #     colour_rgb = (0,0,0)



        # for c in contours:
        #     area = cv2.contourArea(c)
        #     epsilon = 0
        #     if(self.use_trackbars):
        #         Thresholds.AREA_MIN = cv2.getTrackbarPos("AREA MIN", "Parameters")
        #         Thresholds.AREA_MAX = cv2.getTrackbarPos("AREA MAX", "Parameters")
        #         Thresholds.SHAPE_POINTS = cv2.getTrackbarPos("SHAPE POINTS", "Parameters")
        #         epsilon = cv2.getTrackbarPos("CONTOURS", "Parameters")
        #     if(area > Thresholds.AREA_MIN and area < Thresholds.AREA_MAX):
        #         perimeter = cv2.arcLength(c,True)
        #         approx = cv2.approxPolyDP(c, epsilon*perimeter, True) # Corner points
        #         # cv2.drawContours(self.original_cap, [approx], 0, colour_rgb, 5)
        #         bbox = cv2.boundingRect(approx)
        #         x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        #         bbox_pts = np.float32([[x,y], [x+w, y+h], [x+w, y], [x, y+h]]) # TL = x,y, TR = x+w, y, BL = x,y+h, BR = x+w, y+h

        #         center = (int(x+w/2-20),int(y+h/2+5))

        #         cv2.rectangle(img, (x,y), ((x+w), (y+h)), colour_rgb,3,1)
                
                 


        #         cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, colour_rgb, 2)
        #         cv2.putText(img, "Height: " + str(int(h)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, colour_rgb, 2)
        #         cv2.putText(img, "Width: " + str(int(w)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, colour_rgb, 2)
        #         # cv2.putText(img, colour_text, center,  cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,0), 2)
        

        
        
              

    def run_vision_modes(self):
        for modes in self.vision_modes:
            modes()
