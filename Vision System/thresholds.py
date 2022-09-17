import cv2

class Thresholds():
    def __init__(self, colour_arr):
        self.colour = colour_arr

    EDGE_THRESHOLD1 = 150
    EDGE_THRESHOLD2 = 255

    HUE_MIN = 0
    HUE_MAX = 179
    SAT_MIN = 0
    SAT_MAX = 255
    VALUE_MIN = 0
    VALUE_MAX = 255

    EROSION = 0
    EROSION_MAX = 100
    DILATION = 0
    DILATION_MAX = 100

    INCHWORM = [84,79,65]
    LAWNGREEN = [90, 100, 49]
    BRIGHTGREEN = [96,100,50]
    CELADON = [123,47,78]
    PASTELGREEN = [120, 60, 67]
    PISTACHIO = [96, 42, 61]
    DOLLARBILL = [133,187,101]


    

