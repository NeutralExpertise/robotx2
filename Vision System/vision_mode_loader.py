class Vision_Mode_Loader:

    def __init__(self):
        self.vision_modes = []

    def add_mode(self, mode):
       self.vision_modes.append(mode)

    def stream(self, obj_matrix):
        matrix = self.vision_modes[0].stream(obj_matrix)
        for mode in range(len(self.vision_modes)):
            matrix = self.vision_modes[mode].stream(matrix)
        return matrix
            
            
