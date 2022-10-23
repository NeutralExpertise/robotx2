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
def main():

    # Fix position_handler - the functionality is coupled to the stream itself
    # Fix the tracker
    # Add duplicate checking (because there may be race conditions)
    # Add colour based tracking bboxes
        # Detect the center pixel, this should be enough to determine what threshold it sits within (therefore we can then pass the message of the detected black buoy)
    # Change masks to consider greater range of colours
    # Add conditions to send to object handler to determine colour
    # Integrate with message system
        # Send message when black buoy has been identified
        # Send mobility messages based on distance and boundary thresholds
        # x coordinate of each object and determine mobility accordingly
        # If intrusion on left side, left side is smaller X so move right
        # If intrusion on right side, right side is larger X so move left
        # if distance inequality on left side, move right
        # If distance inequality on right side, move left
        # (If one distance is smaller than the other)




    object_handler = Object_Handler()
    object_detector = Object_Detector(object_handler)
    position_handler = Position_Handler()
    object_detector.add_detection_mode(Colour_Detector(object_handler, False))
    object_detector.add_detection_mode(Edge_Detector(object_handler, False))
    object_tracker = Object_Tracker(object_handler)
    




    stream = Stream(object_detector, object_tracker, position_handler, plot_all_object_data=True)
    stream.set_file_path("Resources/ocean-buoys.jpg")
    stream.set_stream_type(Stream_Types.IMAGE)
    stream.set_camera(0)
    # stream.add_trackbars() # - For Testing Only


    stream.start()

 




main()