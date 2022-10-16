import cv2
import keyboard
from stream_settings import Stream_Settings
from stream_types import Stream_Types

class Stream(Stream_Settings):


    def start(self):
        self.is_active = True
        if(self.stream_type == Stream_Types.CAMERA):
            cap = cv2.VideoCapture(self.cameraID)
            if(cap.isOpened() == False):
                print("ERROR: No Camera Found!")
                return
            delay = 1
            while True:
                self.capture = cap.read()[1]
                self.modified_capture = self.capture

                if(len(self.vision_modes) > 0):
                    for mode in self.vision_modes:
                        mode()
                self.display_focal_point()
                cv2.imshow("CAMERA VIEW ", self.capture)
                if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                    break

        elif(self.stream_type == Stream_Types.IMAGE):
            while True:
                try:
                    self.capture = cv2.imread(self.path)
                    self.modified_capture = self.capture
                    if(len(self.vision_modes) > 0):
                        for mode in self.vision_modes:
                            mode()
                    self.display_focal_point()
                    delay = 1
                    cv2.imshow("IMAGE VIEW", self.capture)
                    if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                         break
                except Exception as e:
                    print(e)
                    return