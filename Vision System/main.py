from stream import Stream
from stream_types import Stream_Types
from stream_settings import Stream_Settings
import colour_picker as cp

def main():
    stream = Stream()
    stream.add_type(Stream_Types.CAMERA)
    stream.add_image_path("Resources/buoy.jpg")
    stream.add_camera(0)

    stream.colour_detection()
    stream.edge_detection()
    stream.add_trackbars()
    stream.stream()

    




    


                 

main()