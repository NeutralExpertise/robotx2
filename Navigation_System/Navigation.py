import can
import frc
import GPS_Module

def initialise_can():
    global canBus
    canBus = frc.FrcCan('can0', 'socketcan')

    # Append all listeners
    # APPEND SELF LISTENER (LISTENS TO MESSAGES SENT TO ITSELF
    # APPEND GPS LISTENER
    # canBus.targets.append([A, B, C])

def get_location():
    # GET GPS
    # RETURN GPS

def move_boat(x, y, rotation, power):
    """"
    Function used to perform general movement actions
    """
    # canBus.sendMessage()
    # return true


def move_boat_to_coordinate(gps_lat, gps_lon):
    """
    Function used to move to a specific GPS coordinate. Has no innate collision detection.
    NOTE: REQUIRES TOLERANCE LEVEL FOR ADJUSTMENTS TO STOP
    """
    # GET GPS
    # PERFORM VECTOR CALCULATION
    # move_boat(X,Y,0,Z)

def realign():
    """
    Function used to hold the boat in a specific heading.
    NOTE: REQUIRES TOLERANCE LEVEL FOR ADJUSTMENTS TO STOP
    """
    # GET HEADING
    # PERFORM ROTATIONAL CALCULATION
    # move_boat(0,0,R,P)

    # if (within tolerance):
    # return true

def hold_position(coordinates):
    """
    Function used to hold the boat in a specific location.
    Intended to be used in conjunction with get_location() to hold position at the location that the function was called.
    E.g. hold_position(get_location())
    NOTE: REQUIRES TOLERANCE LEVEL FOR ADJUSTMENTS TO STOP
    """
    # realign()
    # move_boat_to_coordinate(coordinates[0],coordinates[1])

    # if (within tolerance):
    # return true

