import cv2
import numpy as np
class Thresholds():
    def __init__(self, colour_arr):
        self.colour = colour_arr


    EDGE_THRESHOLD1 = 150
    EDGE_THRESHOLD2 = 255

    HUE_MIN = 0
    HUE_MAX = 255
    SAT_MIN = 0
    SAT_MAX = 255
    VALUE_MIN = 0
    VALUE_MAX = 255

    AREA_MIN = 0
    AREA_MAX = 1000000

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
    RED_UPPER = np.array([255,255, 255])
    '''BUOY IS BETTER IDENTIFIED WITH THESE THRESHOLDS'''
    RED_LOWER = np.array([1, 0, 0])
    RED_UPPER = np.array([255,255, 255])
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    GREEN_LOWER = np.array([9, 96, 0])
    GREEN_UPPER = np.array([88, 255, 247])
    WHITE_LOWER = np.array([0, 0, 88])
    WHITE_UPPER = np.array([255, 76, 255])  
    BLACK_LOWER = np.array([0, 0 ,0])
    BLACK_UPPER = np.array([0, 0, 77])

    SHAPE_POINTS = 0
    SHAPE_POINTS_MAX = 9
        
    # Probably add accessors and mutators at some point    



    

