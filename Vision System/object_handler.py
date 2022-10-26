from object import Object
from thresholds import Thresholds
'''Object Handler that "handles" captured objects'''
class Object_Handler:

    def __init__(self):
        self.objects = []
        self.object = Object()
        self.colour_labels = {str(tuple(Thresholds.RED_LOWER)): "RED", str(tuple(Thresholds.GREEN_LOWER)): "GREEN", str(tuple(Thresholds.WHITE_LOWER)): "WHITE", 
        str(tuple(Thresholds.BLACK_LOWER)): "BLACK"}

    def add_colour_data(self, colour_data):
        self.object.colour_label = self.colour_labels[str(colour_data)]
        self.object.set_colour(colour_data)

    def get_colour(self):
        return self.object.get_colour()

    def add_corner_data(self, corner_data):
        self.object.corners = corner_data

    def get_corner_data(self):
        return self.object.get_num_corners()

    def add_coordinates_data(self, coordinate_data):
        self.object.coordinates = coordinate_data

    def get_coordinates(self):
        return self.object.get_coordinates()

    def add_object_to_list(self):
        self.objects.append(self.object)
        self.object = Object()


    def clear_object_list(self):
        self.objects.clear()

    def get_objects(self):
        return self.objects

    def add_distance_data(self, distance):
         self.object.set_distance(distance)

    def get_distance(self):
        return self.object.get_distance()

    def calculate_distance(self, start, end):
        self.object.calculate_distance(start, end)

    def add_boundaries(self):
        self.object.set_boundaries()

    def get_boundaries(self):
        return self.object.get_boundaries()



    

    