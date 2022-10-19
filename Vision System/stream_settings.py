import cv2
from stream_types import Stream_Types
from thresholds import Thresholds
class Stream_Settings():

    def __init__(self):
        self.capture = None
        self.modified_capture = None
        self.path = None
        self.stream_type = Stream_Types.CAMERA
        self.cameraID = 0
        self.is_active = False
        self.object_detection_settings = []
        
         
    def display_focal_point(self):
            cv2.circle(self.capture, (self.get_focal_point_coords()), 10, (0,255,0), 2)

    def get_focal_point_coords(self):
            height, width, _ = self.capture.shape
            cx = int(width/2)
            cy = int(height/2)
            focal_point = (cx,cy)
            return focal_point

    
    def set_capture(self, new_capture):
        self.capture = new_capture
        self.object_detector.stream = new_capture


    def get_capture(self):
        return self.capture
        

    def set_stream_type(self, new_type):
        self.stream_type = new_type

    def set_file_path(self, path):
        self.path = path

    
    def set_camera(self, cameraID):
        self.cameraID = cameraID

    

    # Detection Strategies

    def add_colour_detection(self):
        self.object_detection_settings.append(self.object_detector.add_colour_detection)

    def add_edge_detection(self):
        self.object_detection_settings.append(self.object_detector.add_edge_detection)

    def add_object_tracking(self):
        self.object_detection_settings.append(self.object_detector.add_object_tracking)

    # def resize(self):
    #     if(self.is_active == False):
    #         self.object_detection_settings.append(self.resize)
    #     else:
    #         if(self.use_trackbars):
    #             Thresholds.RESOLUTION_WIDTH, Thresholds.RESOLUTION_HEIGHT = cv2.getTrackbarPos("SIZE WIDTH", "Parameters"), cv2.getTrackbarPos("SIZE HEIGHT", "Parameters")
    #         # WIDTH, HEIGHT CANNOT BE 0 - IMPOSSIBLE
    #         if(Thresholds.RESOLUTION_WIDTH == 0):
    #             Thresholds.RESOLUTION_WIDTH = 1
    #         if(Thresholds.RESOLUTION_HEIGHT == 0):
    #             Thresholds.RESOLUTION_HEIGHT = 1    
    #         self.capture = cv2.resize(self.capture, (Thresholds.RESOLUTION_WIDTH, Thresholds.RESOLUTION_HEIGHT))



    
   


    