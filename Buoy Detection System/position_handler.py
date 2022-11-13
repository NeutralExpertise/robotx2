import cv2
import Navigation


class Position_Handler:


    def __init__(self, object_handler, nav):
        self.object_handler = object_handler
        self.navigation = nav
        self.detect_black_buoy = False
        self.shutdown = False
        self.gate = 0
        
        

        # X:1, Y:0 = right
        # X-1: Y:0 = left
        # X:0 Y:1 = forwards
        # X:0 Y:-1 = backwards   
        # X:0, Y:0 = hold position    

        # Power 1 = full speed
        # Power 0 = stop

        # If gate 1 - move left
        # If gate 2 = forward
        # If gate 3 = move right


    def get_distance_key(self, obj):
        return obj.get_distance()


    def sort_distance(self):
        self.object_handler.get_objects().sort(key=self.get_distance_key)   


    def move(self, x,y,power):
        self.navigation.align_heading()
        self.navigation.move_boat(x,y,rotation,power)
        


    def check_gate(self, obj1, obj2):
        obj1_colour = obj1.get_colour()
        obj2_colour = obj2.get_colour()
        gate_1 = ["GREEN", "WHITE"]
        gate_2 = ["WHITE"]
        gate_3 = ["RED", "WHITE"]

        if(obj1_colour == gate_1[0] or obj2_colour == gate_1[0]):
            self.gate = 1
        if(obj1_colour == gate_2[0] and obj2_colour == gate_2[0]):
            self.gate = 2
        if(obj1_colour == gate_3[0] or obj2_colour == gate_3[0]):
            self.gate = 3


    def align_with_black_buoy(self, focal_point):
        # If the black buoy is not in view - move according to the gate we exited out of
        if(len(self.object_handler.get_objects()) == 0):
            if(self.gate == 1):
                self.move(-1, 0, 0, 1)
            elif(self.gate == 3):
                self.move(1, 0, 0, 1)
        # Black buoy is in view
        else:
            obj = self.object_handler.get_objects()[0]
            x = obj.get_boundaries()[0][0]
            y = obj.get_boundaries()[0][1]
            w = obj.get_boundaries()[1][0]
            h = obj.get_boundaries()[1][1]
            center = (int(x+50),int(y+100))
            
            if(focal_point[0] != center[0]):
                # If x coordinate of buoy is greater than x of the focal point - move left (Object is on our right)
                if(center > focal_point[0]):
                    x = -1
                    y = 0
                    power = 1
                    self.move(x,y,power)
                # x coordinate of buoy is less than x of the focal point - move right (Object is on our left)
                else:
                    x = 1
                    y = 0
                    power = 1
                    self.move(x,y,power)
            else:
                self.move(0,0,0) # HOLD POSITION
                self.detect_black_buoy = False
                self.shutdown = True
                

            

    '''Determines whether the boat needs readjustment
    # The boat is considered to be constantly moving forward UNTIL it is centered and powered down (power 0)
    # The boat is considered to be incorrectly positioned IF:
            # The distance between one object to the focal point is not equal to that of the other object (making up the gate)
            # Only one object is in view AND is NOT a black buoy
    
    '''
    def adjust_position(self, focal_point):
        self.sort_distance()
       
        # Forward
        x = 0
        y = 1
        power = 1
        
        
        if(len(self.object_handler.get_objects()) >= 2):
                self.is_past_gate = False
                # If the x coordinate where the distance is smaller is maximum, then MOVE LEFT (We are too far right)
                # If the x coordinate where the distance is smaller is minimum, then MVOE RIGHT (We are too far left)
                # Re-adjust X amount of units
                
                if(self.object_handler.get_objects()[0].get_coordinates()[0] > self.object_handler.get_objects()[1].get_coordinates()[0]):
                    
                    self.check_gate(self.object_handler.get_objects()[0], self.object_handler.get_objects()[1])
                    x = -1  # LEFT - -1, 0
                    y = 0
                    return (x,y)
                    
                else:
                    x = 1 # RIGHT - 1, 0
                    y = 0
                    return (x,y)
        
        # If only a single buoy is detected - the other side of the gate is out of view
        else:
            if(len(self.object_handler.get_objects()) == 1):
                object = self.object_handler.get_objects()[0]
                if(object.get_colour() != "BLACK"):
                    # If x coordinate of buoy is greater than x of the focal point - move left (Object is on our right)
                    if(object.get_coordinates()[0] >= focal_point[0]):
                        x = -1
                        y = 0
                        return (x,y)
                    # x coordinate of buoy is less than x of the focal point - move right (Object is on our left)
                    else:
                        x = 1
                        y = 0
                        return (x,y)
        
        return None


    # Check for distance inequality
    def check_distances(self, focal_point):
                # Just immediately check for readjustments
                if(self.detect_black_buoy == False):
                    readjustment = self.adjust_position(focal_point)
                    if(readjustment != None):
                        self.move(readjustment[0], readjustment[1], 1)
                    else:
                        self.move(0,1,1)
                else:
                    self.align_with_black_buoy(focal_point)


    # Check if focal point enter's an object's boundary zone
    def check_boundaries(self, focal_point):
        if(self.detect_black_buoy == False):
            readjustment = self.adjust_position(focal_point)
            if(readjustment != None):
                for i in range(len(self.object_handler.get_objects())):
                    obj = self.object_handler.get_objects()[i]
                    x = obj.get_boundaries()[0][0]
                    y = obj.get_boundaries()[0][1]
                    w = obj.get_boundaries()[1][0]
                    h = obj.get_boundaries()[1][1]
                    if(focal_point[0] >= x and 
                    focal_point[0] <= w and 
                    focal_point[1] >= y and 
                    focal_point[1] <= h):
                        self.move(readjustment[0], readjustment[1], 1)
            else:
                self.move(0,1,1)
        else:
            self.align_with_black_buoy(focal_point)
                
                
                

                    

                    
                
                    
                    

            
