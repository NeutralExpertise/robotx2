from stream import Stream_Settings
class Object_Detector(Stream_Settings):

    def __init__(self, object_handler):
        self.detection_modes = []
        self.object_handler = object_handler


    def add_detection_mode(self, detection_mode):
        self.detection_modes.append(detection_mode)

    def remove_detection_mode(self, detection_mode):
        self.detection_modes.remove(detection_mode)



    # Send each capture of the stream to each detector
    def detect(self, stream):
        capture = stream
        for mode in self.detection_modes:
            capture = mode.detect(capture)



