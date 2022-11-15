import cv2
import keyboard
from stream_settings import Stream_Settings
from stream_types import Stream_Types
from position_handler import Position_Handler
import numpy as np
from os import system, name
class Stream(Stream_Settings):

    def __init__(self, source=0, position_handler=None, stream_type=Stream_Types.CAMERA, object_detector=None, plot_focal_point=False,
    plot_focal_point_link=False, plot_object_distance=False, plot_object_coordinates=False, 
    plot_object_size=False, plot_num_object_corners=False, plot_object_box=False, 
    plot_object_boundaries=False, plot_all_object_data=False):
        Stream_Settings.__init__(self, source, stream_type)
        self.plot = []
        self.object_detector = object_detector
        self.position_handler = position_handler
        self.is_active = False



        if(plot_all_object_data == True):
            self.plot.append(self.plot_all_object_data)
        else:
            if(plot_focal_point == True):
                self.plot.append(self.plot_focal_point)
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
            if(plot_object_box == True):
                 self.plot.append(self.plot_object_box)
            if(plot_object_boundaries == True):
                self.plot.append(self.plot_object_boundaries)

      


    def start(self):
        self.is_active = True
        if(self.position_handler != None):
            self.position_handler.shutdown = False
            self.position_handler.detect_black_buoy = False
            if(self.position_handler.get_gate() == None):
                self.position_handler.gate = 0
        # Clear output
        # for windows
        
        if name == 'nt':
            _ = system('cls')
 
        # for mac and linux
        else:
            _ = system('clear')

        print("Starting Stream")

        cap = None
        # Initializing The Stream
        if(self.stream_type == Stream_Types.CAMERA or self.stream_type == Stream_Types.VIDEO):
            cap = cv2.VideoCapture(self.source)
            cap.set(cv2.CAP_PROP_FPS, 60)
            if(self.stream_type == Stream_Types.CAMERA):
                if(cap.isOpened() == False):
                    print("ERROR: No Camera Found - Restarting...")
                    self.start()

        else:
            cap = cv2.imread(self.source)

        # Constantly read frames from the stream
        while True:
            
            if(self.stream_type == Stream_Types.IMAGE):
                self.capture = cv2.imread(self.source)
            else:
                self.capture = cap.read()[1]

            if(self.object_detector != None):
                    if(self.position_handler != None):
                        if(self.position_handler.shutdown == False):
                            self.object_detector.detect(self.capture, self.get_focal_point_coords())
                        else:

                            self.stop_stream()
                    else:
                        self.object_detector.detect(self.capture, self.get_focal_point_coords())

                    if(self.position_handler != None):
                        self.check_position()
                    self.display_data()

            cv2.imshow("STREAM", self.capture)
            if cv2.waitKey(1) and self.is_active == False:
                break
            self.object_detector.object_handler.clear_list()
            
           
    def stop_stream(self):
        self.is_active == False
        cv2.destroyAllWindows()      
            
    
    def check_position(self):
            if(self.position_handler != None):
                    self.position_handler.check_distances(self.get_focal_point_coords())
                    if(self.position_handler.detect_black_buoy == False):
                        self.position_handler.check_boundaries(self.get_focal_point_coords())
                    
                    
        
            

            
    def display_data(self):
        for data in self.plot:
            data()

    def plot_focal_point(self):
        cv2.circle(self.capture, (self.get_focal_point_coords()), 10, (0,255,0), 2)


    def plot_focal_point_link(self):
        for object in self.object_detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                center = (int(x+w/2),int(y+h/2))
                cv2.line(self.capture, (center), (self.get_focal_point_coords()), (255,0,255), 2)


    def plot_object_distance(self):
        for object in self.object_detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                center = (int(x+w/2),int(y+h/2))
                distance = object.get_distance()
                bbox_corner_pts = ((x,y), ((x+w), (y+h)))
                cv2.putText(self.capture, ((str(distance))), (center[0]-20, y-50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0), 3)
                cv2.putText(self.capture, ((str(distance))), (center[0]-20, y-50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)
                cv2.putText(self.capture, ("units"), (center[0]-20, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0), 3)
                cv2.putText(self.capture, ("units"), (center[0]-20, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)




    def plot_object_boundaries(self):
            for object in self.object_detector.object_handler.get_objects():
                if(len(object.get_boundaries()) != 0):
                    cv2.rectangle(self.capture, object.get_boundaries()[0], object.get_boundaries()[1], (85,51,255),5,1)
    



    def plot_object_coordinates(self):
        for object in self.object_detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                cv2.putText(self.capture, "x: " + str(x), (x-20, y+150), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(self.capture, "y: " + str(y), (x-20, y+170), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                


    def plot_object_size(self):
        for object in self.object_detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                cv2.putText(self.capture, "Height: " + str(int(h)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(self.capture, "Width: " + str(int(w)), (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)

    def plot_object_box(self):
        for object in self.object_detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                cv2.rectangle(self.capture, (x, y), (w, h), (255,255,255),3,1)
                


    def plot_num_object_corners(self):
        for object in self.object_detector.object_handler.get_objects():
            if(len(object.get_coordinates()) != 0):
                x = object.get_coordinates()[0]
                y = object.get_coordinates()[1]
                w = object.get_coordinates()[2]
                h = object.get_coordinates()[3]
                center = (int(x+w/2),int(y+h/2))
                cv2.putText(self.capture, "Points: " + str(object.get_corners()), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)



    def plot_all_object_data(self):
        self.plot_object_box
        self.plot_focal_point()
        self.plot_object_distance()
        self.plot_object_coordinates()
        self.plot_focal_point_link()
        self.plot_num_object_corners()
        self.plot_object_size()
        self.plot_object_boundaries()
