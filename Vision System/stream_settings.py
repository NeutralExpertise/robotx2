import cv2
from stream_types import Stream_Types
from thresholds import Thresholds
class Stream_Settings:

    def __init__(self):
        self.capture = None
        self.path = None
        self.stream_type = Stream_Types.CAMERA
        self.cameraID = 0
        self.is_active = False
        
        
         

    def get_focal_point_coords(self):
        height, width, _ = self.capture.shape
        cx = int(width/2)
        cy = int(height/2)
        focal_point = (cx,cy)
        return focal_point

    

    
    def set_capture(self, new_capture):
        self.capture = new_capture


    def get_capture(self):
        return self.capture
        

    def set_stream_type(self, new_type):
        self.stream_type = new_type

    def set_file_path(self, path):
        self.path = path

    
    def set_camera(self, cameraID):
        self.cameraID = cameraID


        '''FOR TESTING PURPOSES ONLY'''
    def add_trackbars(self):
        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 1000, 500)
        cv2.createTrackbar("EDGE THRESHOLD1", "Parameters", Thresholds.EDGE_THRESHOLD1, Thresholds.EDGE_THRESHOLD2, self.on_value_change) # 255
        cv2.createTrackbar("EDGE THRESHOLD2", "Parameters", Thresholds.EDGE_THRESHOLD2, Thresholds.EDGE_THRESHOLD2, self.on_value_change) # 139

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

        cv2.createTrackbar("CORNER POINTS MIN", "Parameters", Thresholds.CORNER_POINTS_MIN, Thresholds.CORNER_POINTS_MAX, self.on_value_change)
        cv2.createTrackbar("CORNER POINTS MAX", "Parameters", Thresholds.CORNER_POINTS_MAX, Thresholds.CORNER_POINTS_MAX, self.on_value_change)


    '''FOR TESTING PURPOSES ONLY'''
    def on_value_change(self, val):
        pass


    



    
   


    