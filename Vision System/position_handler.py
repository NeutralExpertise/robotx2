import cv2
class Position_Handler:

    def __init__(self, object_handler):
        self.object_handler = object_handler


    def check_distance_violation(self, stream):
        if(len(self.object_handler.get_objects()) == 2):
            objects = list(self.object_handler.get_objects())
            if(objects[0].get_distance() != objects[1].get_distance()):
                cv2.putText(stream, "BOUNDARY VIOLATION ", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 10)
                cv2.putText(stream, "BOUNDARY VIOLATION ", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                return True
        return False
            


    # Check if focal point enter's an object's boundary zone (Means boat is not centered)
    def check_boundary_violation(self, stream):
        focal_point = self.get_focal_point_coords()
        for object in self.objects:
            x = object.get_coordinates()[0][0]
            y = object.get_coordinates()[0][1]
            w = object.get_coordinates()[1][0]
            h = object.get_coordinates()[1][1]
            if(self.get_focal_point_coords()[0] >= x and 
            self.get_focal_point_coords()[0] <= w and 
            self.get_focal_point_coords()[1] > y and 
            self.get_focal_point_coords()[1] < h):
                cv2.putText(stream, "BOUNDARY VIOLATION ", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 10)
                cv2.putText(stream, "BOUNDARY VIOLATION ", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                return True
        else:
            cv2.putText(stream, "", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 10)
            cv2.putText(stream, "", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        return False


    def check_violations(self):
        distance_violation = self.check_distance_violation()
        boundary_violation = self.check_boundary_violation()



    def plot_object_boundaries(self):
        cv2.rectangle(self.capture, self.boundaries[0], self.boundaries[1], (85,51,255),10,1)