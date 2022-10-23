import cv2
from thresholds import Thresholds
import numpy as np
class Colour_Detector():


    def __init__(self, object_handler, use_trackbars):
        self.use_trackbars = use_trackbars
        self.object_handler = object_handler


    def remove_shadows(self, capture):
        colour_planes = cv2.split(capture)
        normalized_planes = []
        for plane in colour_planes:
            dilated_capture = cv2.dilate(plane, np.ones((7,7), np.uint8))
            # smooth the image
            smooth_blur = cv2.medianBlur(dilated_capture, 21)
            # difference between the colour_plane and the smoothed image
            difference = 255 - cv2.absdiff(plane, smooth_blur)
            # modify the intensity values of the pixels so they can be more easily seen
            norm_capture = cv2.normalize(difference, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            normalized_planes.append(norm_capture)
        shadows_removed = cv2.merge(colour_planes)
        return shadows_removed


    def remove_glare(self, capture):
        # convert to gray
        gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)

        # threshold grayscale image to extract glare
        mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)[1]

        # Optionally add some morphology close and open, if desired
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)


        # use mask with input to do inpainting (restore the extracted region)
        result = cv2.inpaint(capture, mask, 21, cv2.INPAINT_TELEA)
        return result




  

    def detect(self, capture):
        # result = self.remove_glare(capture)
        # result = self.remove_shadows(result)
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
        

        
    

        colour_detected_capture = cv2.bitwise_and(capture, capture, mask = mask) # Merge the original with the mask


        if(self.use_trackbars):
            cv2.imshow("COLOUR DETECTOR", colour_detected_capture)
            cv2.imshow("MASK", mask)
             
        return colour_detected_capture
