import cv2

from stream_types import Stream_Types


class Stream():

    

    def __init__(self, stream_type, path=None, cameraID = 0):
        if(stream_type.name not in Stream_Types.__members__):
            raise Exception("ERROR: Invalid Stream Type")
        self.path = path
        self.cameraID = cameraID
        self.stream_type = stream_type

        

    # Set the stream type (Video, Image, Camera Stream etc...)
    def set_type(self, new_type):
        self.stream_type = new_type

    # Get the stream type
    def get_type(self):
        return self.stream_type


    '''
    Start up a stream according to the stream type

    Params: vision_mode = Determines if the stream captures unique specifications (such as edge detecting or colour detector or both)
    
    '''
    def stream(self, vision_mode = None):
        # Stream is camera
        if(self.stream_type == Stream_Types.CAMERA):
            self.stream_type = cv2.VideoCapture(self.cameraID)
            delay = 1
            while True:
                self.stream_cap = self.stream_type.read()[1]
                if(vision_mode != None):
                    vision_mode()
                cv2.imshow("CAMERA VIEW ", self.stream_cap)
                # Quit if 'q' is presssed
                if cv2.waitKey(delay) & 0xFF ==ord('q'):
                    break
        
        # Stream is a static image
        elif(self.stream_type == Stream_Types.IMAGE):
            try:
                self.stream_type = cv2.imread(self.path)
                delay = 0
                # if(vision_method != None):
                #     vision_method()
                cv2.imshow("IMAGE VIEW", self.stream_type)
                cv2.waitKey(delay)
            except Exception as e:
                print(e)
                
        # Stream is a video (.mp4, .wav etc..)
        elif(self.stream_type == Stream_Types.VIDEO):
            try:
                self.stream_type = cv2.VideoCapture(self.path)
                self.stream_type = self.stream_type.read()[1]
                delay = 1
                while True:
                    cv2.imshow("VIDEO VIEW", self.stream_type)
                    # Quit if 'q' is presssed
                    if cv2.waitKey(delay) & 0xFF ==ord('q'):
                        break
            except:
                    print("Error: Path Not Found")






        

   

        
            
