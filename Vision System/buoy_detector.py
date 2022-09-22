from re import S
from stream_settings import Stream_Settings
from stream import Stream
class Buoy_Detector(Stream_Settings):
    def __init__(self, camera = 0):
        self.stream = Stream()
        self.stream.cameraID = self.stream.add_camera(0)
        self.stream.colour_detection()
        self.stream.edge_detection()
        self.stream.contour_detector()

    def run():
        pass

    # Need to identify colour
        # Need to scan over the object and find the majority colour
            # Identify whether colour is one of the colours we need to look for
            # Need to identify contours
                # Deploy contour detector over the coloured objects
                    # Get the x,y,w,h of the object
                        # Deploy a bounding box
                            # Points
