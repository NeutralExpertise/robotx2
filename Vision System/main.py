import cv2
from stream import Stream
from stream_types import Stream_Types
def main():
    stream = Stream()

    # stream.add_trackbars()
    stream.set_image_path("Resources/ocean-buoys.jpg")
    stream.set_stream_type(Stream_Types.CAMERA)
    stream.object_tracker()
    stream.colour_detection()
    stream.edge_detection()



    stream.start()



main()