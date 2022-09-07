from abc import abstractclassmethod


class IVision_Mode:
    @abstractclassmethod
    def stream(self, obj_matrix):
        pass


