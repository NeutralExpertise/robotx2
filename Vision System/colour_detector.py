import cv2
from thresholds import Thresholds
class Colour_Detector():


    def __init__(self, object_handler, use_trackbars):
        self.use_trackbars = use_trackbars
        self.object_handler = object_handler
  


    def detect(self, capture):
        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)

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

        colour_detected_capture = cv2.bitwise_and(capture, capture, mask = mask) # Merge the original with the mask
        if(self.use_trackbars):
            cv2.imshow("COLOUR DETECTOR", colour_detected_capture)
            cv2.imshow("MASK", mask)
        object_colour = [0,0,0]   
        self.object_handler.add_colour_data(object_colour)        
        return colour_detected_capture
