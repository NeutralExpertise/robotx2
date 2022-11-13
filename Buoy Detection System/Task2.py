import can
import frc
import GPS_Module
import Navigation
from robotx_buoy_detector import RobotX_Buoy_Detector


# class task_info:
# def __init__(self):
#    self.gate_used = 0


def initialise_can():
    global canBus
    canBus = frc.FrcCan('can0', 'socketcan')
    # Gate Movement Listener
    canBus.targets.append([20, 8, 1])


def main():
    # Initialise can connection
    initialise_can()

    while True:
        # LISTENING FOR CAN SIGNAL
        # IF SIGNAL TO BEGIN TASK 2
        if canBus.gate.enabled == 1:
            print("Commencing Task 2")
            enter_course()

            # IF SIGNAL TO COMPLETE COURSE
            print("Commencing course exit")
            exit_course()
        else:
            Navigation.stop()


def enter_course():
    # waypoint_1 = [0, 0]
    # waypoint_2 = [0, 0]
    # waypoint_3 = [0, 0]
    # waypoint_4 = [0, 0]
    # waypoint_5 = [0, 0]
    buoy_detector = RobotX_Buoy_Detector(False)  # Set to True to perform testing

    # ASSUMPTION: POSITIONED BETWEEN FIRST GATE
    # STEP 1- MOVE TOWARDS FIRST GATE
    # ACCESS VISION SYSTEM/GPS
    Navigation.NORTHBOUND = Navigation.get_heading()
    buoy_detector.stream.start()
    # WHILE BOAT INCORRECT DISTANCE FROM GATE - GOTO 1

    # STEP 2- ADJUST BOAT POSITION TO BE EQUIDISTANT FROM BUOYS
    # ACCESS VISION SYSTEM/GPS
    # WHILE BOAT IN INCORRECT POSITION, GOTO 2

    # STEP 3- ACCESS VISION SYSTEM/GPS
    # MOVE BOAT TILL BETWEEN BUOYS
    # ACCESS BEACON SCANNER
    # WHILE NO SIGNAL DETECTED, MOVE BOAT BACKWARDS AND SIDEWAYS TO NEXT GATE, THEN GOTO 3

    # MOVE THROUGH GATE
    # STEP 4- ACCESS VISION SYSTEM/GPS
    # REPOSITION TO BLACK BUOY BASED ON GATE ENTERED
    # WHILE BOAT IN INCORRECT POSITION, GOTO 4

    # ASSUMPTION - 5M FROM BLACK BUOY
    # LOOP AROUND BUOY
    Navigation.align_heading(Navigation.NORTHBOUND)

    Navigation.move_boat_by_distance('right', 2.5)
    Navigation.move_boat_by_distance('left', 5)
    Navigation.move_boat_by_distance('left', 5)
    Navigation.move_boat_by_distance('left', 5)
    Navigation.move_boat_by_distance('left', 2.5)

    Navigation.align_heading(Navigation.heading_calculator(Navigation.NORTHBOUND, 180))
    # NOW FACING GATES AGAIN


def exit_course():
    buoy_detector = RobotX_Buoy_Detector(False)  # Set to True to perform testing

    buoy_detector.stream.start()
    # ASSUMPTION: BOAT GUIDED TO EXIT
    # STEP 1- ACCESS VISION SYSTEM/GPS
    # RECALL GATE USED FROM TASK_INFO CLASS
    # POSITION BOAT IN FRONT OF USED GATE

    # STEP 2- ADJUST BOAT POSITION TO BE EQUIDISTANT FROM BUOYS
    # ACCESS VISION SYSTEM/GPS
    # WHILE BOAT IN INCORRECT POSITION, GOTO 2

    # EXIT COURSE


if __name__ == '__main__':
    main()
