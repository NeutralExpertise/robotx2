import cv2
import numpy as np
from screeninfo import get_monitors
class Thresholds():
    resolution = {"top": get_monitors()[0].y, "left":get_monitors()[0].x, "height": get_monitors()[0].height, "width":get_monitors()[0].width}

    EDGE_THRESHOLD1 = 0
    EDGE_THRESHOLD2 = 234

    HUE_MIN = 0
    HUE_MAX = 255
    SAT_MIN = 0
    SAT_MAX = 255
    VALUE_MIN = 0
    VALUE_MAX = 255

    AREA_MIN = 100
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

    CORNER_POINTS = 8

    RESOLUTION_HEIGHT = resolution["height"]
    RESOLUTION_WIDTH = resolution["width"]


    # RED_LOWER = np.array([161,20, 60])
    # RED_UPPER = np.array([255,255, 255])
    '''BUOY IS BETTER IDENTIFIED WITH THESE THRESHOLDS'''
    RED_LOWER = np.array([0, 97, 0])
    RED_UPPER = np.array([13,255, 255])
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    GREEN_LOWER = np.array([17, 0, 0])
    GREEN_UPPER = np.array([84, 255, 2184])
    WHITE_LOWER = np.array([255, 255, 255])
    WHITE_UPPER = np.array([255, 255, 164])  
    BLACK_LOWER = np.array([0, 0 ,0])
    BLACK_UPPER = np.array([0, 0, 77])

    SHAPE_POINTS = 0
    SHAPE_POINTS_MAX = 9 



    
