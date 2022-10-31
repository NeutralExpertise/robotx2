import numpy as np
from screeninfo import get_monitors
class Thresholds:
    


    EDGE_THRESHOLD1 = 0
    EDGE_THRESHOLD2 = 255

    HUE_MIN = 0
    HUE_MAX = 180
    SAT_MIN = 0
    SAT_MAX = 255
    VALUE_MIN = 0
    VALUE_MAX = 255

    SAT_ADD = 0
    SAT_REDUCE = 0
    VALUE_ADD = 0
    VALUE_REDUCE = 0

    AREA_MIN = 0
    AREA_MAX = 1000000
    HEIGHT_MIN = 0
    HEIGHT_MAX = 1000
    WIDTH_MIN = 0
    WIDTH_MAX = 1000

    EROSION_ITERATIONS_MIN = 1
    EROSION_ITERATIONS_MAX = 10
    DILATION_ITERATIONS_MIN = 1
    DILATION_ITERATIONS_MAX = 10

    DILATION_KERNEL_MIN = 5
    DILATION_KERNEL_MAX = 5
    EROSION_KERNEL_MIN = 5
    EROSION_KERNEL_MAX = 5

    BLUR_KERNEL_MIN = 5
    BLUR_KERNEL_MAX = 5

    CORNER_POINTS_MIN = 0
    CORNER_POINTS_MAX = 20



    def set_hue(self, lower_threshold, upper_threshold):
        self.HUE_MIN = lower_threshold
        self.HUE_MAX = upper_threshold

    def set_saturation(self, lower_threshold, upper_threshold):
        self.SAT_MIN = lower_threshold
        self.SAT_MAX = upper_threshold

    def set_value(self, lower_threshold, upper_threshold):
        self.VALUE_MIN = lower_threshold
        self.VALUE_MAX = upper_threshold

    def get_hue(self):
        return (self.HUE_MIN, self.HUE_MAX)

    def get_saturation(self):
        return (self.SAT_MIN, self.SAT_MAX)

    def get_value(self):
        return (self.VALUE_MIN, self.VALUE_MAX)

    
    def set_edge_thresholds(self, lower_threshold, upper_threshold):
        self.EDGE_THRESHOLD1 = lower_threshold
        self.EDGE_THRESHOLD2 = upper_threshold

    def set_corner_thresholds(self, lower_threshold, upper_threshold):
        self.CORNER_POINTS_MIN = lower_threshold
        self.CORNER_POINTS_MAX = upper_threshold

    def set_area_thresholds(self, lower_threshold, upper_threshold):
        self.AREA_MIN = lower_threshold
        self.AREA_MAX = upper_threshold

    def set_blur_kernel(self, kernel_min, kernel_max):
        self.BLUR_KERNEL_MIN = kernel_min
        self.BLUR_KERNEL_MAX = kernel_max
        
    def set_erosion_kernel(self, kernel_min, kernel_max):
        self.EROSION_KERNEL_MIN = kernel_min
        self.EROSION_KERNEL_MAX = kernel_max

    def set_dilation_kernel(self, kernel_min, kernel_max):
        self.DILATION_KERNEL_MIN = kernel_min
        self.DILATION_KERNEL_MAX = kernel_max

    def set_erosion_iterations(self, min_iterations, max_iterations):
        self.EROSION_ITERATIONS_MIN = min_iterations
        self.EROSION_ITERATIONS_MAX = max_iterations

    def set_dilation_iterations(self, min_iterations, max_iterations):
        self.DILATION_ITERATIONS_MIN = min_iterations
        self.DILATION_ITERATIONS_MAX = max_iterations


    def set_height(self, min_height, max_height):
        self.HEIGHT_MIN = min_height
        self.HEIGHT_MAX = max_height

    def set_width(self, min_width, max_width):
        self.WIDTH_MIN = min_width
        self.WIDTH_MAX = max_width

    
    def add_saturation(self, new_sat):
        self.SAT_ADD = new_sat

    def reduce_saturation(self, new_sat):
        self.SAT_REDUCE = new_sat

    def add_value(self, new_value):
        self.VALUE_ADD = new_value

    def reduce_value(self, new_value):
        self.VALUE_REDUCE = new_value
