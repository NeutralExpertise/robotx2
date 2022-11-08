import cv2
class Position_Handler:


    def __init__(self, object_handler):
        self.object_handler = object_handler


    def get_distance(self, obj):
        return obj.get_distance()


    def calculate_adjustments(self):
        if(len(self.object_handler.get_objects()) >= 2):
                # Sort objects based on their distance
                self.object_handler.get_objects().sort(key=self.get_distance)
                # If the x coordinate where the distance is smaller is maximum, then MOVE LEFT (We are too far right)
                # If the x coordinate where the distance is smaller is minimum, then MVOE RIGHT (We are too far left)
                # Re-adjust X amount of units
                direction = None
                if(self.object_handler.get_objects()[0].get_coordinates()[0] > self.object_handler.get_objects()[1].get_coordinates()[0]):
                    direction = "LEFT"
                    return (direction, self.object_handler.get_objects()[1].get_distance() - self.object_handler.get_objects()[0].get_distance())
                else:
                    direction = "RIGHT"
                    return (direction, self.object_handler.get_objects()[1].get_distance() - self.object_handler.get_objects()[0].get_distance())

        return None

    # Check for distance inequality
    def check_distances(self, capture, plot_conditional_info=False):
                readjustment = self.calculate_adjustments()
                if(readjustment != None):
                    if(plot_conditional_info == True):
                        
                            
                            cv2.putText(capture, "DISTANCE VIOLATION: MOVE " + readjustment[0], (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 10)
                            cv2.putText(capture, "DISTANCE VIOLATION: MOVE " + readjustment[0], (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                    else:
                        cv2.putText(capture, "", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 10)
                        cv2.putText(capture, "", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)


    # Check if focal point enter's an object's boundary zone
    def check_boundaries(self, capture, focal_point, plot_conditional_info=False):
        readjustment = self.calculate_adjustments()
        if(readjustment != None):
            for i in range(0,2):
                obj = self.object_handler.get_objects()[i]
                x = obj.get_boundaries()[0][0]
                y = obj.get_boundaries()[0][1]
                w = obj.get_boundaries()[1][0]
                h = obj.get_boundaries()[1][1]
                if(focal_point[0] >= x and 
                focal_point[0] <= w and 
                focal_point[1] >= y and 
                focal_point[1] <= h):
                    
                
                    if(plot_conditional_info == True):
                            
                            cv2.putText(capture, "BOUNDARY VIOLATION: MOVE " + readjustment[0], (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 10)
                            cv2.putText(capture, "BOUNDARY VIOLATION: MOVE " + readjustment[0], (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

                    else:
                            cv2.putText(capture, "", (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 10)
                            cv2.putText(capture, "", (500,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                    

            