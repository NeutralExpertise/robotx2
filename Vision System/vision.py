import cv2
from stream import Stream
from trackbars import Trackbars

class Vision(Stream):

     
    
    def __init__(self, stream_type, track_thresholds=False, edge_threshold1 = 100, edge_threshold2 = 100):
        Stream.__init__(self, stream_type)
        self.trackbars = None
        if(track_thresholds == True):
            self.trackbars = Trackbars()
        self.edge_thresholds = [edge_threshold1, edge_threshold2]

    def set_thresholds(self, t1, t2):
        self.edge_thresholds[0] = t1
        self.edge_thresholds[1] = t2

    def get_thresholds(self):
        return self.edge_thresholds   

    # Function that executes when value of track bars change - pass to do nothing
    def on_value_change(self, value):
        pass


    def detect_colour(self):
        return

    # Edge detector
    def detect_edges(self):
            stream_colour = self.change_colour(self.stream_cap)
            blur = self.blur(stream_colour)
            # No Trackbars
            if(self.trackbars == None):
                self.edge_thresholds[0] = 100
                self.edge_thresholds[1] = 100

            elif(self.trackbars != None): 
                # Avoids duplicate windows
                if(self.trackbars.is_active == False):
                    self.trackbars.create_window()
                # Track threshold changes
                else:
                    self.edge_thresholds[0] = cv2.getTrackbarPos("Threshold1", "Parameters") 
                    self.edge_thresholds[1] = cv2.getTrackbarPos("Threshold2", "Parameters")

            self.stream_cap = cv2.Canny(blur, self.edge_thresholds[0], self.edge_thresholds[1])


    # Change the colour of the output
    def change_colour(self, matrix):
        return cv2.cvtColor(matrix, cv2.COLOR_BGR2GRAY)

    # Blur the stream
    def blur(self, matrix):
        return cv2.GaussianBlur(matrix, (7,7), 1)
        