import cv2

from stream_types import Stream_Types

class Stream():

    

    def __init__(self, stream_type, vision_mode=None, path=None, cameraID = 0):
        if(stream_type.name not in Stream_Types.__members__):
            raise Exception("ERROR: Invalid Stream Type")
        self.vision_mode = vision_mode
        self.path = path
        self.cameraID = cameraID
        self.stream_type = stream_type



    def stream(self):
        # Stream is a camera
        if(self.stream_type == Stream_Types.CAMERA):
            self.stream_type = cv2.VideoCapture(self.cameraID)
            delay = 1
            while True:
                cap = self.stream_type.read()[1]
                if(self.vision_mode != None):
                    adjusted_cap = self.vision_mode.stream(cap)
                cv2.imshow("CAMERA VIEW ", adjusted_cap)
                if cv2.waitKey(delay) & 0xFF ==ord('q'):
                        break
                          
             # Stream is a static image
        elif(self.stream_type == Stream_Types.IMAGE):
            try:
                self.stream_type = cv2.imread(self.path)
                delay = 0
                if(self.vision_mode != None):
                    self.stream_cap = self.vision_mode.stream(self.stream_cap)
                cv2.imshow("IMAGE VIEW", self.stream_type)
                cv2.waitKey(delay)
            except Exception as e:
                print(e)
                
        # Stream is a video (.mp4, .wav etc..)
        elif(self.stream_type == Stream_Types.VIDEO):
            try:
                self.stream_type = cv2.VideoCapture(self.path)
                cap = self.stream_type.read()[1]
                delay = 1
                if(self.vision_mode != None):
                    adjusted_cap = self.vision_mode.stream(cap)
                while True:
                    cv2.imshow("VIDEO VIEW", adjusted_cap)
                    # Quit if 'q' is presssed
                    if cv2.waitKey(delay) & 0xFF ==ord('q'):
                        break
            except:
                    print("Error: Path Not Found")

        



        

   

        
            
