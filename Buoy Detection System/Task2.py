import can
import frc
import GPS_Module
import Navigation
from robotx_buoy_detector import RobotX_Buoy_Detector

# import HEARTBEAT_MONITOR

# class task_info:
# def __init__(self):
#    self.gate_used = 0

GPS_METER = 0.00000900900900


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
        print("Commencing Task 2")
        enter_course()

        # IF SIGNAL TO COMPLETE COURSE
        print("Commencing course exit")
        exit_course()


def enter_course():
    waypoint_1 = [0, 0]
    waypoint_2 = [0, 0]
    waypoint_3 = [0, 0]
    waypoint_4 = [0, 0]
    waypoint_5 = [0, 0]
    buoy_detector = RobotX_Buoy_Detector(False)  # Set to True to perform testing

    # ASSUMPTION: POSITIONED BETWEEN FIRST GATE
    # STEP 1- MOVE TOWARDS FIRST GATE
    # ACCESS VISION SYSTEM/GPS
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
    waypoint_1 = Navigation.get_location()
    Navigation.move_boat_to_coordinate(waypoint_2[0], waypoint_2[1])
    Navigation.move_boat_to_coordinate(waypoint_3[0], waypoint_3[1])
    Navigation.move_boat_to_coordinate(waypoint_4[0], waypoint_4[1])
    Navigation.move_boat_to_coordinate(waypoint_5[0], waypoint_5[1])
    Navigation.move_boat_to_coordinate(waypoint_1[0], waypoint_1[1])

    # POSSIBLY REALIGN_HEADING HERE
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