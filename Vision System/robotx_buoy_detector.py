from colour_detector import Colour_Detector
from edge_detector import Edge_Detector
from object import Object
from object_detector import Object_Detector
from object_handler import Object_Handler
from object_tracker import Object_Tracker
from position_handler import Position_Handler
from stream import Stream
from stream_types import Stream_Types
from thresholds import Thresholds
from screeninfo import get_monitors
'''THIS IS A PRE-BUILT PROFILE FOR THE ROBOTX ENTRANCE AND EXIT GATE TASK'''
class RobotX_Buoy_Detector:
    def __init__(self):
        self.object_handler = Object_Handler()
        self.position_handler = Position_Handler()
        red = ((120, 65, 0), (180,255,255)) 
        green = ((28, 142, 0), (85, 255, 255))
        white = ((0, 0, 200), (180, 35, 255))
        black = ((0 , 0 , 0), (0, 0 , 77))
        self.thresholds = Thresholds()
        self.thresholds.set_edge_thresholds(0, 255)
        self.thresholds.set_area_thresholds(550, 100000)
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
        self.colour_detector = Colour_Detector(self.object_handler, self.thresholds, False)
        self.object_detector = Object_Detector(self.object_handler, use_trackbars=False, thresholds=self.thresholds)
        self.object_detector.add_colour(red[0], red[1], "RED")
        self.object_detector.add_colour(green[0], green[1], "GREEN")
        self.object_detector.add_colour(white[0], white[1], "WHITE")
        self.object_detector.add_colour(black[0], black[1], "BLACK")

        # self.colour_detector.add_colour(black[0], black[1], "BLACK")
        # self.object_detector.add_detection_mode(self.colour_detector)

        # self.edge_detector = Edge_Detector(self.object_handler, self.thresholds, True)
        # self.object_detector.add_detection_mode(self.edge_detector)
        # MultiTracker Is Too CPU Intensive!
        # object_tracker = None
        # if(self.colour_detector.use_trackbars != True and self.edge_detector.use_trackbars != True):
        #     object_tracker = Object_Tracker(self.object_handler)                                  
        
        self.stream = Stream(self.object_detector, tracker=None, position_handler=self.position_handler, plot_all_object_data=True)
        self.stream.set_file_path("Resources/boundary_violation.png")
        self.stream.set_stream_type(Stream_Types.IMAGE)
        self.stream.set_camera(0)
        self.stream.set_resolution(get_monitors()[0].y, get_monitors()[0].x, get_monitors()[0].height, get_monitors()[0].width)

        self.stream.start()