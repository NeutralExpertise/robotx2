from colour_detector import Colour_Detector
from edge_detector import Edge_Detector
from stream import Stream
from stream_types import Stream_Types
from vision_mode_loader import Vision_Mode_Loader
from Ivision_mode import IVision_Mode

def main():
    edge_detector = Edge_Detector(track_thresholds=True)
    colour_detector = Colour_Detector()

    vision_modes = Vision_Mode_Loader()
    vision_modes.add_mode(colour_detector)
    vision_modes.add_mode(edge_detector)

    stream = Stream(Stream_Types.CAMERA, vision_modes)
    stream.stream()
    


main()