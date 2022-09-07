from Ivision_mode import IVision_Mode
import cv2
class Colour_Detector(IVision_Mode):

    def stream(self, obj_matrix):
        grey_scale = self.change_colour(obj_matrix)
        blurred = self.blur(obj_matrix)
        return blurred
       

    def change_colour(self, matrix):
        return cv2.cvtColor(matrix, cv2.COLOR_BGR2GRAY)


    # Blur the stream
    def blur(self, matrix):
        return cv2.GaussianBlur(matrix, (7,7), 1)