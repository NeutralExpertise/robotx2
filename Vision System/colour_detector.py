import cv2
from thresholds import Thresholds
import numpy as np
import imutils
class Colour_Detector():


    def __init__(self, object_handler, colours_to_detect, use_trackbars):
        self.use_trackbars = use_trackbars
        self.object_handler = object_handler
        self.colours = colours_to_detect # (LOWER, UPPER) : COLOUR_STRING.


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
        capture = self.remove_glare(capture)
        capture = self.remove_shadows(capture)
        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)

        if(self.use_trackbars):

            Thresholds.RED_LOWER[0] = Thresholds.HUE_MIN = cv2.getTrackbarPos("HUE MIN", "Parameters")
            Thresholds.RED_LOWER[1] = Thresholds.SAT_MIN = cv2.getTrackbarPos("SAT MIN", "Parameters")
            Thresholds.RED_LOWER[2] = Thresholds.VALUE_MIN = cv2.getTrackbarPos("VALUE MIN", "Parameters")
            Thresholds.RED_UPPER[0] = Thresholds.HUE_MAX = cv2.getTrackbarPos("HUE MAX", "Parameters")
            Thresholds.RED_UPPER[1] = Thresholds.SAT_MAX = cv2.getTrackbarPos("SAT MAX", "Parameters")
            Thresholds.RED_UPPER[2] = Thresholds.VALUE_MAX = cv2.getTrackbarPos("VALUE MAX", "Parameters")

        t = 0
        red = ((170, 130, 80), (255,255,255))
        
        # for colour in self.colours:
        #     colour # The entire key
        #     colour[0] # T1
        #     colour[0][0] # T2
        #     colour[0][0][0] # First element of T1

        #     print(self.colours[colour])

        # red_mask = cv2.inRange(hsv, Thresholds.RED_LOWER, Thresholds.RED_UPPER)
        # green_mask = cv2.inRange(hsv, Thresholds.GREEN_LOWER, Thresholds.GREEN_UPPER)
        # white_mask = cv2.inRange(hsv, Thresholds.WHITE_LOWER, Thresholds.WHITE_UPPER)
        # black_mask = cv2.inRange(hsv, Thresholds.BLACK_LOWER, Thresholds.BLACK_UPPER)

        # mask = red_mask + green_mask + white_mask + black_mask
        # mask = red_mask

        # self.__contour_detection(red_mask, Thresholds.RED_LOWER)
        # self.__contour_detection(green_mask, Thresholds.GREEN_LOWER)
        # self.__contour_detection(white_mask, Thresholds.WHITE_LOWER)
        # self.__contour_detection(black_mask, Thresholds.BLACK_LOWER)
    

        colour_detected_capture = cv2.bitwise_and(capture, capture, mask = mask) # Merge the original with the mask


        if(self.use_trackbars):
            cv2.imshow("COLOUR DETECTOR", colour_detected_capture)
            cv2.imshow("MASK", mask)
             
        return colour_detected_capture


    def __contour_detection(self, capture, colour):
        colour = (int(colour[0]), int(colour[1]), int(colour[2]))
        conts = cv2.findContours(capture, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        conts = imutils.grab_contours(conts)
        if(self.use_trackbars):
            Thresholds.AREA_MIN = cv2.getTrackbarPos("AREA MIN", "Parameters")
            Thresholds.AREA_MAX = cv2.getTrackbarPos("AREA MAX", "Parameters")
            Thresholds.CORNER_POINTS_MIN = cv2.getTrackbarPos("CORNER POINTS MIN", "Parameters")
            Thresholds.CORNER_POINTS_MAX = cv2.getTrackbarPos("CORNER POINTS MAX", "Parameters")
            
        max_bbox = 0
        for c in conts:
            perimeter = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c, 0.02*perimeter, True) # Corner points
            bbox = cv2.boundingRect(approx)
            x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            bbox_pts = np.float32([[x,y], [x+w, y+h], [x+w, y], [x, y+h]]) # TL = x,y, TR = x+w, y, BL = x,y+h, BR = x+w, y+h

            center = (int(x+w/2),int(y+h/2)) # Center of bbox
            
            # Reduce the detection so only a set size of objects can be detected
            if(cv2.contourArea(c) > Thresholds.AREA_MIN and cv2.contourArea(c) < Thresholds.AREA_MAX):
                # The buoys usually have 8 corner points
                if(len(approx) > Thresholds.CORNER_POINTS_MIN and len(approx) < Thresholds.CORNER_POINTS_MAX):
                    # Only display a box over the object itself and ignore all the shapes detected INSIDE the object itself
                    if(h > max_bbox):
                        bbox_corner_pts = ((x,y), ((x+w), (y+h)))
                        self.object_handler.add_corner_data(len(approx))
                        self.object_handler.add_coordinates_data((bbox_corner_pts[0][0], bbox_corner_pts[0][1], w, h))
                        # self.object_handler.add_coordinates_data(bbox)
                        self.object_handler.add_boundaries()
                        self.object_handler.add_colour_data(colour)

                        self.object_handler.add_object_to_list()
                        max_bbox = h
