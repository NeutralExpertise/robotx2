import cv2
class Object():
    coordinates = ()
    boundaries = (())
    distance = 0
    colour = []
    corners = 0

    def set_num_corners(self, corners):
        self.corners = corners


    def get_num_corners(self):
        return self.corners


    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_coordinates(self):
        return self.coordinates

    def set_boundaries(self, pt1, pt2):
        
        #     # Object Avoidance Boundaries
            pt1 = (int(self.coordinates[0]-100), int(self.coordinates[1]-100)) # x,y
            pt2 = (int(self.coordinates[0] + self.coordinates[2])+100, int(self.coordinates[1] + self.coordinates[3])+100) # w,h
            self.boundaries.add((pt1, pt2))


    def get_boundaries(self):
        return self.boundaries


    def calculate_distance(self, p1,p2):
        distance = int(((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5)


    def get_distance(self):
        return self.distance


    def plot_focal_point_link(self, stream, focal_point):
        x = self.coordinates[0][0]
        y = self.coordinates[0][1]
        w = self.coordinates[1][0]
        h = self.coordinates[1][1]
        center = (int(x+w/2),int(y+h/2))
        cv2.line(stream, (center), (focal_point), (255,0,255), 2)


    def plot_coordinates(self, stream):
        x = self.coordinates[0][0]
        y = self.coordinates[0][1]
        w = self.coordinates[1][0]
        h = self.coordinates[1][1]
        cv2.putText(stream, "x: " + str(x), (x + w + 20, y + 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(stream, "y: " + str(y), (x + w + 20, y + 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)

    def plot_size(self, stream):
        x = self.coordinates[0][0]
        y = self.coordinates[0][1]
        w = self.coordinates[1][0]
        h = self.coordinates[1][1]
        cv2.putText(stream, "Height: " + str(int(h)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(stream, "Width: " + str(int(w)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)


    def plot_num_corners(self, stream):
        x = self.coordinates[0][0]
        y = self.coordinates[0][1]
        w = self.coordinates[1][0]
        h = self.coordinates[1][1]
        center = (int(x+w/2),int(y+h/2))
        cv2.putText(stream, str(self.distance), (center), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0), 2)
        cv2.putText(stream, "Points: " + str(self.corners), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)

    def plot_boundaries(self, stream):
        cv2.rectangle(stream, self.boundaries[0], self.boundaries[1], (85,51,255),10,1) 

    def plot_data(self):
        self.plot_boundaries()
        self.plot_coordinates()
        self.plot_focal_point_link()
        self.plot_num_corners()
        self.plot_size()
