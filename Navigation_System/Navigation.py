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


def hold_position():
    """
    Function used to hold the boat in a specific location.
    NOTE: REQUIRES TOLERANCE LEVEL FOR ADJUSTMENTS TO STOP
    """
    # GET GPS
    # PERFORM VECTOR CALCULATION
    # if (within tolerance):
    # return true


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
