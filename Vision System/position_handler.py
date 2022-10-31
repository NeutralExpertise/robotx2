import cv2
from stream_settings import Stream_Settings
class Position_Handler(Stream_Settings):


    def check_distance_violation(self, obj_1, obj_2):
        if(obj_1.get_distance() != obj_2.get_distance()):
            return True
            
        return False

            

    # Check if focal point enter's an object's boundary zone
    def check_boundary_violation(self, obj, focal_point):
        x = obj.get_boundaries()[0][0]
        y = obj.get_boundaries()[0][1]
        w = obj.get_boundaries()[1][0]
        h = obj.get_boundaries()[1][1]
        if(focal_point[0] >= x and 
        focal_point[0] <= w and 
        focal_point[1] >= y and 
        focal_point[1] <= h):
            return True
        
        return False

