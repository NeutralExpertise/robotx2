from object import Object

'''Object Handler that "handles" a single object'''
class Object_Handler:

    def __init__(self):
        self.objects = set([])
        self.object = Object()

    def add_colour_data(self, colour_data):
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
        for object in self.objects:
            if(object.get_coordinates() == self.object.get_coordinates()):
                return
        self.objects.add(self.object)

    def clear_object_list(self):
        self.objects.clear()

    def get_objects(self):
        return self.objects

    def add_distance_data(self, distance):
         self.object.set_distance(distance)

    def get_distance(self):
        return self.object.get_distance()

    

    