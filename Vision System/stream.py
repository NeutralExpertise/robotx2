import cv2
import keyboard
from stream_settings import Stream_Settings
from stream_types import Stream_Types

class Stream(Stream_Settings):



    def stream(self):
        # Stream is a camera
        if(self.stream_type == Stream_Types.CAMERA):
            cap = cv2.VideoCapture(self.cameraID)
            delay = 1
            while True:
                self.original_cap = cap.read()[1]
                self.stream_cap = self.original_cap
                if(len(self.vision_modes) > 0):
                    self.run_vision_modes()
                cv2.imshow("CAMERA VIEW ", self.stream_cap)
                if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                    break
                          
             # Stream is a static image
        elif(self.stream_type == Stream_Types.IMAGE):
            try:
                cap = cv2.imread(self.path)
                delay = 0
                cv2.imshow("IMAGE VIEW", cap)
                cv2.waitKey(delay)
            except Exception as e:
                print(e)
                
        # Stream is a video (.mp4, .wav etc..)
        elif(self.stream_type == Stream_Types.VIDEO):
            try:
                cap = cv2.VideoCapture(self.path)
                self.original_cap = cap.read()[1]
                delay = 1
                if(len(self.vision_modes) > 0):
                    self.run_vision_modes()
                while True:
                    cv2.imshow("VIDEO VIEW", self.stream_cap)
                    # Quit if 'q' is presssed
                    if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                        break
            except:
                    print("Error: Path Not Found")

        



        

   

        
            
