import cv2
'''Object Class
# Gets updated as each detector returns their related information, for example colour detector will update the object's colour

'''
class Object():
    def __init__(self):
        self.coordinates = ()
        self.boundaries = (())
        self.distance = 0
        self.colour = []
        self.corners = 0

    def set_num_corners(self, corners):
        self.corners = corners


    def get_num_corners(self):
        return self.corners


    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour


    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_coordinates(self):
        return self.coordinates

    def set_boundaries(self, pt1, pt2):
        
            # Object Avoidance Boundaries
            pt1 = (int(self.coordinates[0]-100), int(self.coordinates[1]-100)) # x,y
            pt2 = (int(self.coordinates[0] + self.coordinates[2])+100, int(self.coordinates[1] + self.coordinates[3])+100) # w,h
            self.boundaries.add((pt1, pt2))


    def get_boundaries(self):
        return self.boundaries


    def calculate_distance(self, p1,p2):
        distance = int(((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5)


    def get_distance(self):
        return self.distance

