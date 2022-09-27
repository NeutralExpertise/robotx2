import cv2
import numpy as np
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

    AREA_MIN = 0
    AREA_MAX = 20000

    EROSION = 1
    EROSION_MAX = 100
    DILATION = 1
    DILATION_MAX = 100

    DILATION_KERNEL = 5
    DILATION_KERNEL_MAX = 5
    EROSION_KERNEL = 5
    EROSION_KERNEL_MAX = 5

    BLUR_KERNEL = 5
    BLUR_KERNEL_MAX = 5


    RED_LOWER = np.array([161,20, 60])
    RED_UPPER = np.array([179,255, 255])
    '''RED BUOY IS BETTER IDENTIFIED WITH THESE THRESHOLDS'''
    # RED_LOWER = np.array([0,148, 0])
    # RED_UPPER = np.array([179,255, 255])
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    GREEN_LOWER = np.array([45, 20, 60])
    GREEN_UPPER = np.array([90, 255, 255])
    WHITE_LOWER = np.array([0, 0, 135])
    WHITE_UPPER = np.array([179, 18, 255])
    BLACK_LOWER = np.array([0, 0 ,0])
    BLACK_UPPER = np.array([179, 45, 85])

    SHAPE_POINTS = 0
    SHAPE_POINTS_MAX = 9
        
    # Probably add accessors and mutators at some point    



    

