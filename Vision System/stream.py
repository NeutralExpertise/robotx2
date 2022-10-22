import cv2
import keyboard
from stream_settings import Stream_Settings
from stream_types import Stream_Types

class Stream(Stream_Settings):

    def __init__(self, detector, tracker, 
    plot_focal_point_link=False, plot_object_distance=False, plot_object_coordinates=False, 
    plot_object_size=False, plot_num_object_corners=False, plot_object_colour=False, plot_all_object_data=False):
        self.plot = []
        self.detector = detector
        self.tracker = tracker
        if(plot_all_object_data == True):
            self.plot.append(self.plot_all_object_data)
        else:
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
                self.detector.detect(self.capture)
                self.tracker.track(self.capture)
                if(self.capture.shape != None):
                    self.display_focal_point()
                self.display_data()
                self.detector.object_handler.add_object_to_list()
                cv2.imshow("CAMERA VIEW ", self.capture)
                cv2.waitKey(1)
                if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                    break

        elif(self.stream_type == Stream_Types.IMAGE):
            while True:
                try:
                    self.capture = cv2.imread(self.path)
                    self.detector.detect(self.capture)
                    self.tracker.track(self.capture)
                    if(self.capture.shape != None):
                        self.display_focal_point()
                    self.display_data()
                    self.detector.object_handler.add_object_to_list()
                    delay = 1
                    cv2.imshow("IMAGE VIEW", self.capture)
                    if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                         break
                except Exception as e:
                    print(e)
                    return
        elif(self.stream_type == Stream_Types.VIDEO):
                try:
                    cap = cv2.VideoCapture(self.path)
                    cap.set(cv2.CAP_PROP_FPS, 120)
                    while True:
                        self.capture = cap.read()[1]
                        self.detector.detect(self.capture)
                        self.tracker.track(self.capture)
                        if(self.capture.shape != None):
                            self.display_focal_point()
                        self.display_data()
                        self.detector.object_handler.add_object_to_list()
                        delay = 1
                        cv2.imshow("VIDEO VIEW", self.capture)
                        cv2.waitKey(2)
                        if cv2.waitKey(delay) and keyboard.is_pressed("q"):
                            break
                except Exception as e:
                    print(e)
                    return



    def display_data(self):
        for data in self.plot:
            data()



    def plot_focal_point_link(self):
        x = self.detector.object_handler.get_coordinates()[0]
        y = self.detector.object_handler.get_coordinates()[1]
        w = self.detector.object_handler.get_coordinates()[2]
        h = self.detector.object_handler.get_coordinates()[3]
        center = (int(x+w/2),int(y+h/2))
        cv2.line(self.capture, (center), (self.get_focal_point_coords()), (255,0,255), 2)


    def plot_object_distance(self):
        pass



    def plot_object_coordinates(self):
        x = self.detector.object_handler.get_coordinates()[0]
        y = self.detector.object_handler.get_coordinates()[1]
        w = self.detector.object_handler.get_coordinates()[2]
        h = self.detector.object_handler.get_coordinates()[3]
        cv2.putText(self.capture, "x: " + str(x), (x + w + 20, y + 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(self.capture, "y: " + str(y), (x + w + 20, y + 120), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)


    def plot_object_size(self):
        x = self.detector.object_handler.get_coordinates()[0]
        y = self.detector.object_handler.get_coordinates()[1]
        w = self.detector.object_handler.get_coordinates()[2]
        h = self.detector.object_handler.get_coordinates()[3]
        cv2.putText(self.capture, "Height: " + str(int(h)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(self.capture, "Width: " + str(int(w)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)

    


    def plot_num_object_corners(self):
        x = self.detector.object_handler.get_coordinates()[0]
        y = self.detector.object_handler.get_coordinates()[1]
        w = self.detector.object_handler.get_coordinates()[2]
        h = self.detector.object_handler.get_coordinates()[3]
        center = (int(x+w/2),int(y+h/2))
        cv2.putText(self.capture, str(self.detector.object_handler.get_distance()), (center), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0), 2)
        cv2.putText(self.capture, "Points: " + str(self.detector.object_handler.get_corner_data()), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)




    def plot_object_colour(self):
        x = self.detector.object_handler.get_coordinates()[0]
        y = self.detector.object_handler.get_coordinates()[1]
        # cv2.putText(self.capture, "Points: " + str(self.detector.object_handler.get_corner_data()), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)

    def plot_all_object_data(self):
        self.plot_object_colour()
        self.plot_object_coordinates()
        self.plot_focal_point_link()
        self.plot_num_object_corners()
        self.plot_object_size()