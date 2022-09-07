from Ivision_mode import IVision_Mode
import trackbars
import cv2
class Edge_Detector(IVision_Mode):

    def __init__(self, thresholds=[100,100], track_thresholds=False):
        self.thresholds = thresholds
        if(track_thresholds):
            self.trackbars = trackbars.Trackbars()
        else:
            self.trackbars = None
        


    def stream(self, obj_matrix):
        if(self.trackbars != None and not self.trackbars.is_active):
            self.trackbars.create_window()
        if(self.trackbars != None and self.trackbars.is_active):
            self.thresholds[0] = cv2.getTrackbarPos("Threshold1", "Parameters") 
            self.thresholds[1] = cv2.getTrackbarPos("Threshold2", "Parameters")            
        return cv2.Canny(obj_matrix, self.thresholds[0], self.thresholds[1])
       
        