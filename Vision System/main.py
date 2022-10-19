import cv2
from object_detector import Object_Detector
from stream import Stream
from stream_types import Stream_Types
def main():
    stream = Stream()
    # stream.add_trackbars()
    stream.set_file_path("Resources/ocean-buoys.jpg")
    stream.set_stream_type(Stream_Types.IMAGE)
    stream.add_colour_detection()
    stream.add_edge_detection()
    stream.add_object_tracking()
    stream.start()



main()