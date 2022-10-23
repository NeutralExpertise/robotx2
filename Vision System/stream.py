from turtle import position
import cv2
import keyboard
from stream_settings import Stream_Settings
from stream_types import Stream_Types

class Stream(Stream_Settings):

    def __init__(self, detector, tracker, position_handler, plot_focal_point=False,
    plot_focal_point_link=False, plot_object_distance=False, plot_object_coordinates=False, 
    plot_object_size=False, plot_num_object_corners=False, plot_object_colour=False, plot_object_boundaries=False, plot_focal_point_violation_reporting=False, plot_all_object_data=False):
        self.plot = []
        self.detector = detector
        self.tracker = tracker
        self.position_handler = position_handler
        
        if(plot_all_object_data == True):
            self.plot.append(self.plot_all_object_data)
        else:
            if(plot_focal_point == True):
                self.plot(self.plot_focal_point)
            if(plot_focal_point_link == True):
                self.plot.append(self.plot_focal_point_link)
            if(plot_object_distance == True):
                self.plot.append(self.plot_object_distance)
            if(plot_object_coordinates == True):
                self.plot.append(self.plot_object_coordinates)
            if(plot_object_size == True):
                self.plot.append(self.plot_object_size)
            if(plot_num_object_corners == True):
                self.plot.append(self.plot_num_object_corners)
            if(plot_object_colour == True):
                 self.plot.append(self.plot_object_colour)
            if(plot_object_boundaries == True):
                self.plot.append(self.plot_object_boundaries)
            if(plot_focal_point_violation_reporting == True):
                self.plot.append(self.plot_focal_point_violation_reporting)






    def start(self):
        self.is_active = True
        if(self.stream_type == Stream_Types.CAMERA):
            cap = cv2.VideoCapture(self.cameraID)
            cap.set(cv2.CAP_PROP_FPS, 60)
            if(cap.isOpened() == False):
                print("ERROR: No Camera Found!")
                return
            delay = 1
            while True:
                self.capture = cap.read()[1]
                self.handle_object_detection()
                self.display_data()
                cv2.imshow("CAMERA VIEW ", self.capture)
                cv2.waitKey(1)
                if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                    break
                self.detector.object_handler.clear_object_list()

        elif(self.stream_type == Stream_Types.IMAGE):
            while True:
                try:
                    self.capture = cv2.imread(self.path)
                    self.handle_object_detection()
                    self.display_data()
                    delay = 1
                    cv2.imshow("IMAGE VIEW", self.capture)
                    if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                         break
                    self.detector.object_handler.clear_object_list()
                except Exception as e:
                    print(e)
                    return
        elif(self.stream_type == Stream_Types.VIDEO):
                try:
                    cap = cv2.VideoCapture(self.path)
                    cap.set(cv2.CAP_PROP_FPS, 120)
                    while True:
                        self.capture = cap.read()[1]
                        self.handle_object_detection()
                        self.display_data()
                        delay = 1
                        cv2.imshow("VIDEO VIEW", self.capture)
                        cv2.waitKey(1)
                        if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                            break
                        self.detector.object_handler.clear_object_list()
                except Exception as e:
                    print(e)
                    return




    def handle_object_detection(self):
            self.detector.detect(self.capture)
            self.tracker.track(self.capture)
            for object in self.detector.object_handler.get_objects():
                if(len(object.get_coordinates()) != 0):
                    x = object.get_coordinates()[0]
                    y = object.get_coordinates()[1]
                    w = object.get_coordinates()[2]
                    h = object.get_coordinates()[3]
                    center = (int(x+w/2),int(y+h/2))
                    object.calculate_distance(x, self.get_focal_point_coords()[0])




    def display_data(self):
        for data in self.plot:
            data()


    def plot_focal_point(self):
        cv2.circle(self.capture, (self.get_focal_point_coords()), 10, (0,255,0), 2)



    def plot_focal_point_link(self):
        for object in self.detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                center = (int(x+w/2),int(y+h/2))
                cv2.line(self.capture, (center), (self.get_focal_point_coords()), (255,0,255), 2)


    def plot_object_distance(self):
        for object in self.detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                center = (int(x+w/2),int(y+h/2))
                distance = object.get_distance()
                cv2.putText(self.capture, str(distance), (center), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0), 2)



    def plot_object_boundaries(self):
            for object in self.detector.object_handler.get_objects():
                if(len(object.get_boundaries()) != 0):
                    cv2.rectangle(self.capture, object.get_boundaries()[0], object.get_boundaries()[1], (85,51,255),10,1)




    def plot_object_coordinates(self):
        for object in self.detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                cv2.putText(self.capture, "x: " + str(x), (x + w + 20, y + 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(self.capture, "y: " + str(y), (x + w + 20, y + 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)


    def plot_object_size(self):
        for object in self.detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                cv2.putText(self.capture, "Height: " + str(int(h)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(self.capture, "Width: " + str(int(w)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)

    


    def plot_num_object_corners(self):
        for object in self.detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                center = (int(x+w/2),int(y+h/2))
                cv2.putText(self.capture, "Points: " + str(object.get_num_corners()), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)

    
    def plot_focal_point_violation_reporting(self):
        
        if(len(self.detector.object_handler.get_objects()) > 0):
            # Distance violation detection
            if(len(self.detector.object_handler.get_objects()) >= 2):
                objects = list(self.detector.object_handler.get_objects())
                x = self.detector.object_handler.get_objects()[0].get_coordinates()[0]
                y = self.detector.object_handler.get_objects()[0].get_coordinates()[1]
                if(self.position_handler.check_distance_violation(self.capture, self.detector.object_handler.get_objects()[0], self.detector.object_handler.get_objects()[1]) == True):
                    
                    cv2.putText(self.capture, "DISTANCE VIOLATION ", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 10)
                    cv2.putText(self.capture, "DISTANCE VIOLATION ", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                else:
                    cv2.putText(self.capture, "", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 10)
                    cv2.putText(self.capture, "", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        
            # Boundary Violation Detection
            for object in self.detector.object_handler.get_objects():
                if(self.position_handler.check_boundary_violation(self.capture, object, self.get_focal_point_coords()) == True):
                    cv2.putText(self.capture, "BOUNDARY VIOLATION ", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 10)
                    cv2.putText(self.capture, "BOUNDARY VIOLATION ", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

                else:
                    cv2.putText(self.capture, "", (object.get_coordinates()[0], object.get_coordinates()[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 10)
                    cv2.putText(self.capture, "", (object.get_coordinates()[0], object.get_coordinates()[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    def plot_object_colour(self):
        x = self.detector.object_handler.get_coordinates()[0]
        y = self.detector.object_handler.get_coordinates()[1]
        # cv2.putText(self.capture, "Points: " + str(self.detector.object_handler.get_corner_data()), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)

    def plot_all_object_data(self):
        # self.plot_object_colour()
        self.plot_focal_point()
        self.plot_object_distance()
        self.plot_object_coordinates()
        self.plot_focal_point_link()
        self.plot_num_object_corners()
        self.plot_object_size()
        self.plot_object_boundaries()
        self.plot_focal_point_violation_reporting