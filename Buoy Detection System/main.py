from robotx_buoy_detector import RobotX_Buoy_Detector
import Task2
def main():

    #Initialise can connection
    Task2.initialise_can()
    buoy_detector = RobotX_Buoy_Detector(False) # Set to True to perform testing

    while True:
        #LISTENING FOR CAN SIGNAL
        #IF SIGNAL TO BEGIN TASK 2
        print("Commencing Task 2")
        Task2.task_2()
        buoy_detector.stream.start()
        

    
        #IF SIGNAL TO COMPLETE COURSE
        print("Commencing course exit")
        Task2.exit_course()





main()

