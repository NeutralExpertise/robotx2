from turtle import position
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
def main():


    # Integrate with message system
        # Send message when black buoy has been identified
        # Send mobility messages based on distance and boundary thresholds
        # x coordinate of each object and determine mobility accordingly
        # If intrusion on left side, left side is smaller X so move right
        # If intrusion on right side, right side is larger X so move left
        # if distance inequality on left side, move right
        # If distance inequality on right side, move left
        # (If one distance is smaller than the other)


    # Template matching????


    # Identify which gate, gate 1 is (red, white), gate 2 is (white white), gate 3 is (white, green) - Out of scope for now

    # Crop area behind the focal point?

    # To check that we are looking at a gate - The 2 detected (objects) should have a relative even distance range apart AND should be on the same x,y range

    # x,y coord ranges
    # width, height
    # colour - if object is red, look for white, if object is green, look for white, object is white, look for white
    # distance
    # Identify 2 objects in the same x,y range and then check their distances, Identify all objects in the same x,y range, and track them?
        # Check if the distance from an object is greater or less than the height of the x,y range?
        # 


    object_handler = Object_Handler()
    object_detector = Object_Detector(object_handler)
    position_handler = Position_Handler()
    red = ((170, 130, 80), (255,255,255))
    colours = {red: "RED"}
    object_detector.add_detection_mode(Colour_Detector(object_handler, colours,  False))
    # object_detector.add_detection_mode(Edge_Detector(object_handler, False))
    object_tracker = Object_Tracker(object_handler)                                  
    



    stream = Stream(object_detector, tracker=None, position_handler=position_handler, plot_all_object_data=True)
    stream.set_file_path("Resources/robotx.mp4")
    # stream.set_file_path("Resources/ocean-buoys.jpg")
    stream.set_stream_type(Stream_Types.VIDEO)
    stream.set_camera(0)
    # stream.add_trackbars() # - For Testing Only


    stream.start()

 




main()