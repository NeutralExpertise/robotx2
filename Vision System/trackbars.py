import cv2

class Trackbars():

    def __init__(self):
        self.is_active = False

    def on_value_change(self, val):
            pass
    
    def create_window(self):
        self.is_active = True
        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 640, 240)
        cv2.createTrackbar("Threshold1", "Parameters", 150, 255, self.on_value_change)
        cv2.createTrackbar("Threshold2", "Parameters", 255,255, self.on_value_change)


   

