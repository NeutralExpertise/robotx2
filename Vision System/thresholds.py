import cv2

class Thresholds():
    def __init__(self, colour_arr):
        self.colour = colour_arr


    EDGE_THRESHOLD1 = 150
    EDGE_THRESHOLD2 = 255

    COLOUR = ""
    HUE_MIN = 0
    HUE_MAX = 180
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


    WHITE_HUE = 120
    WHITE_SAT = 40
    WHITE_VAL = 255

    RED_HUE = 161
    RED_SAT = 0
    RED_VAL = 255

    ORANGE_HUE = 22
    ORANGE_SAT = 0
    ORANGE_VAL = 255

    YELLOW_HUE = 33
    YELLOW_SAT = 0
    YELLOW_VAL = 255

    GREEN_HUE = 78
    GREEN_SAT = 0
    GREEN_VAL = 255
    
    BLACK_HUE = 100
    BLACK_SAT = 100
    BLACK_VAL = 100

    BLUE_HUE = 120
    BLUE_SAT = 0
    BLUE_VAL = 255

    PURPLE_HUE = 170
    PURPLE_SAT = 0
    PURPLE_VAL = 255

    SHAPE_POINTS = 0
    SHAPE_POINTS_MAX = 9
        
    # Probably add accessors and mutators at some point    

    


    

