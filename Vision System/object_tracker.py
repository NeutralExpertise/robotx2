import cv2

from stream_settings import Stream_Settings
class Object_Tracker(Stream_Settings):

    def __init__(self, object_handler):
        self.tracker = cv2.legacy.MultiTracker.create()
        self.active_tracker = self.create_tracker()
        self.object_handler = object_handler
        self.num_objects_tracking = 0


    def track(self, capture):
        if(self.num_objects_tracking < len(self.object_handler.get_objects())):
            # THIS CODE CAUSES THE TRACKER TO BE TOO SLOW - WE NEED TO ONLY USE IT ON NEW OBJECTS
            for object in self.object_handler.get_objects():
                self.tracker.add(self.active_tracker, capture, object.get_coordinates())
                self.num_objects_tracking += 1
        if(len(self.object_handler.get_objects()) > 0):
            success, bboxes = self.tracker.update(capture)
            if(success):
                cv2.putText(capture, "TRACKING ", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                for object in bboxes:
                    pt1 = (int(object[0]), int(object[1]))
                    pt2 = (int(object[0] + object[2]), int(object[1] + object[3]))
                    cv2.rectangle(capture, pt1, pt2, (255,0,255),3,1)            

            else:
                cv2.putText(capture, "TRACKING LOST", (400, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)


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