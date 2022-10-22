import cv2
from colour_detector import Colour_Detector
from edge_detector import Edge_Detector
from object import Object
from object_detector import Object_Detector
from object_handler import Object_Handler
from object_tracker import Object_Tracker
from stream import Stream
from stream_types import Stream_Types
def main():


    # stream.add_trackbars()
    # Integrate trackbars with new system - 5mins
    # Fix position_handler - 10 mins
    # Maybe add functionality to clear the object list - TBD
    # Change masks to consider greater range of colours - 1hr
    # Add conditions to send to object handler to determine colour - 20min
    # Add considerations for glare and shadows - 1 day
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
    object_detector.add_detection_mode(Colour_Detector(object_handler, False))
    object_detector.add_detection_mode(Edge_Detector(object_handler, False))
    object_tracker = Object_Tracker(object_handler)
    stream = Stream(object_detector, object_tracker, plot_focal_point_link=True)
    stream.set_file_path("Resources/ocean-buoys.jpg")
    stream.set_stream_type(Stream_Types.IMAGE)
    stream.set_camera(0)


    stream.start()

 




main()