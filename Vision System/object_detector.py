objects = set([])
class Object_Detector():


    def get_objects():
        return objects


    def get_object(index):
        try:
            object = objects[index]
            return object
        except IndexError:
            print("Index Out Of Range")   


    def add_object(object):
        objects.add(object)



    








