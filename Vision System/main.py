from stream import Stream
from stream_types import Stream_Types
from vision import Vision

def main():
    vision = Vision(Stream_Types.CAMERA, track_thresholds=True)
    vision.stream(vision.detect_edges)

    


main()

print("hello world")
