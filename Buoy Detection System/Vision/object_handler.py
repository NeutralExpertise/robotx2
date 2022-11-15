from object import Object
'''Object Handler that "handles" captured objects'''
class Object_Handler:

    def __init__(self):
        self.objects = []
        self.object = Object()

    def add_colour(self, colour_data):
        self.object.set_colour(colour_data)

    def get_colour(self):
        return self.object.get_colour()

    def add_corners(self, corner_data):
        self.object.corners = corner_data

    def get_corners(self):
        return self.object.get_corners()

    def add_coordinates(self, coordinate_data):
        self.object.coordinates = coordinate_data

    def get_coordinates(self):
        return self.object.get_coordinates()

    def add_object_to_list(self):
        self.objects.append(self.object)
        self.object = Object()


    def add_area(self, area_data):
        self.object.area = area_data



    def clear_list(self):
        self.objects.clear()

    def get_objects(self):
        return self.objects

    def add_distance_data(self, distance):
         self.object.set_distance(distance)

    def get_distance(self):
        return self.object.get_distance()

    def calculate_distance(self, start, end):
        return self.object.calculate_distance(start, end)

    def add_boundaries(self):
        self.object.set_boundaries()

    def get_boundaries(self):
        return self.object.get_boundaries()
        



    

    