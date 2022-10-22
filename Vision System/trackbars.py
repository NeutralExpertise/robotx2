import cv2
from thresholds import Thresholds
class Trackbars:

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