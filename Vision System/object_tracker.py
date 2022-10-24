import cv2

from stream_settings import Stream_Settings
import numpy as np
class Object_Tracker(Stream_Settings):

    def __init__(self, object_handler):
        self.tracker = cv2.legacy.MultiTracker.create()
        
        self.active_tracker = self.create_tracker()
        self.object_handler = object_handler


    def check_tracked_objects(self, capture):
         # Ensure that we don't add another tracker to an already tracked object
        for object in self.object_handler.get_objects():
            if(object.get_coordinates() not in self.tracker.getObjects()):
                self.tracker.add(self.create_tracker(), capture, object.get_coordinates())                
                   
        

    def track(self, capture):

        
        # Add duplication checking code here
        
        # Update the tracker to track the new location of the object
        success, bboxes = self.tracker.update(capture)
        if(len(self.tracker.getObjects()) > 0):
            if(len(bboxes) > 0):
                if(success):
                    cv2.putText(capture, "TRACKING ", (100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                    for object in bboxes:
                        pt1 = (int(object[0]), int(object[1]))
                        pt2 = (int(object[0] + object[2]), int(object[1] + object[3]))
                        cv2.rectangle(capture, pt1, pt2, (255,0,255),3,1)            

                else:
                    cv2.putText(capture, "TRACKING LOST", (100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                    self.tracker = cv2.legacy.MultiTracker.create()
            

        self.check_tracked_objects(capture)
        
       
        

    def set_tracker(self, tracker):
        self.tracker = tracker            
                    
            
    def create_tracker(self, tracker="CSRT"):
        if(tracker.upper() == "BOOSTING"):
            tracker = cv2.legacy.TrackerBoosting_create()
        elif(tracker.upper() == "MIL"):
            tracker = cv2.legacy.TrackerMIL_create()
        elif(tracker.upper() == "KCF"): 
            tracker = cv2.legacy.TrackerKCF_create()
        elif(tracker.upper() == "TLD"):
            tracker = cv2.legacy.TrackerTLD_create()
        elif(tracker.upper() == "MEDIANFLOW"):
            tracker = cv2.legacy.TrackerMedianFlow_create()
        elif(tracker.upper() == "MOSSE"):
            tracker = cv2.legacy.TrackerMOSSE_create()
        elif(tracker.upper() == "CSRT"):
            tracker = cv2.legacy.TrackerCSRT_create()
        return tracker