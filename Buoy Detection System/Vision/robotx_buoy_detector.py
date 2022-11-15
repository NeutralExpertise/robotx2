from object_detector import Object_Detector
from object_handler import Object_Handler
from position_handler import Position_Handler
from thresholds import Thresholds
from stream import Stream
from stream_types import Stream_Types
from screeninfo import get_monitors
'''THIS IS A PRE-BUILT PROFILE FOR THE ROBOTX ENTRANCE AND EXIT GATE TASK'''
class RobotX_Buoy_Detector:
    def __init__(self, enable_testing=False):
        self.object_handler = Object_Handler()
        '''Thresholds To Determine What Objects Are Detected
        Colours are determined through HSV:
            (Minimum Hue, Minimum Saturation, Minimum Value), (Maximum Hue, Maximum Saturation, Maximum Value)

        
        
        '''
        # HUE_MIN, SAT_MIN, VAL_MIN, HUE_MAX, SAT_MAX, VAL_MAX
        red = ((100, 50, 180), (180,255,255))  
        green = ((75, 40, 150), (90, 255, 255))
        white = ((0, 0, 180), (180, 35, 255))
        black = ((0 , 0 , 0), (180, 255, 81))
        colours = {(red[0], red[1]) : "RED", (green[0], green[1]) : "GREEN", (white[0], white[1]) : "WHITE", (black[0], black[1]) : "BLACK" }
        self.thresholds = Thresholds()
        
        '''Change These For Custom Testing Ranges
        Values are determined as minimum and maximum values
        For example, set_edge_thresholds(0, 255) will allow the entire range from 0 to 255 to be tested
        '''
        self.thresholds.set_edge_thresholds(0, 255)
        self.thresholds.set_area_thresholds(1000, 100000)
        self.thresholds.set_blur_kernel(5,5)
        self.thresholds.set_corner_thresholds(0,15)
        self.thresholds.set_dilation_iterations(1,10)
        self.thresholds.set_erosion_iterations(1,10)
        self.thresholds.set_hue(0,180)
        self.thresholds.set_saturation(0,255)
        self.thresholds.set_value(0,255)
        self.thresholds.set_erosion_kernel(5,5)
        self.thresholds.set_dilation_kernel(13,13)
        self.thresholds.set_height(31,300)

        self.object_detector = Object_Detector(object_handler = self.object_handler, thresholds = self.thresholds, colours_to_detect=colours, use_trackbars=enable_testing)
        self.position_handler = Position_Handler(self.object_handler)                                  
        
        self.stream = Stream(source=0, position_handler=self.position_handler, stream_type=Stream_Types.CAMERA, 
        object_detector=self.object_detector, plot_all_object_data=True)

        '''Source and Resolution
        If testing is required on an image or video:
             Set source to the location of the file path and set stream_type to Stream_Types.IMAGE or Stream_Types.VIDEO
        If a live camera is to be used, set the source to the ID of the camera, for example: The first camera is always 0

        '''
        source = "Resources/test_img.png"
        source = 0
        self.stream.set_source(source) # Set to 0 to use camera
        self.stream.set_stream_type(Stream_Types.CAMERA)
        self.stream.set_resolution(get_monitors()[0].y, get_monitors()[0].x, get_monitors()[0].height, get_monitors()[0].width)