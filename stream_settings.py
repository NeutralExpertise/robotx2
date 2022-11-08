import cv2
from stream_types import Stream_Types
from screeninfo import get_monitors
class Stream_Settings:

    def __init__(self, stream_type=Stream_Types.CAMERA, source=0,):
        self.capture = None
        self.source = source
        self.stream_type = stream_type
        self.resolution = {"top": get_monitors()[0].y, "left":get_monitors()[0].x, "height": get_monitors()[0].height, "width":get_monitors()[0].width}
        

    def get_resolution(self):
        return self.resolution

    def set_resolution(self, top, left, height, width):
        self.resolution = {"top": top, "left": left, "height": height, "width": width}



    def get_focal_point_coords(self):
        height, width, _ = self.capture.shape
        cx = int(width/2)
        cy = int(height/2)
        focal_point = (cx,cy)
        return focal_point

     
    def set_capture(self, new_capture):
        self.capture = new_capture


    def get_capture(self):
        return self.capture
        

    def set_stream_type(self, new_type):
        self.stream_type = new_type

    def set_source(self, source):
        self.source = source



    def set_display_size(self, width, height):
        self.capture = cv2.resize(self.capture, (width, height))

    



    
   


    