import cv2
from stream import Stream
from stream_types import Stream_Types
import colour_picker as cp
def main():
    stream = Stream()
    stream.add_type(Stream_Types.IMAGE)
    stream.add_image_path("Resources/ocean-buoys.jpg")
    stream.add_camera(0)
    # stream.resize()
    stream.colour_detection()
    stream.edge_detection()
    stream.display_focal_point()
    # stream.object_tracking()
    
    stream.add_trackbars()
    stream.stream()

    



                 

main()