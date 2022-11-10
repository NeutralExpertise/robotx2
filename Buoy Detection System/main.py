from robotx_buoy_detector import RobotX_Buoy_Detector

def main():


    buoy_detector = RobotX_Buoy_Detector(False) # Set to True to perform testing
    buoy_detector.stream.start()


main()

