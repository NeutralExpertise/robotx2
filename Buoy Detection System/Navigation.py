import can
import frc
import math
from math import radians, cos, sin, asin, sqrt


TOLERANCE_ROTATIONAL = 0.5      # 0.5 degrees
TOLERANCE_DISTANCE = 0.00001    # 2.22 meters

def initialise_can():
    global canBus
    canBus = frc.FrcCan('can0', 'socketcan')

    # APPEND SELF LISTENER (LISTENS TO MESSAGES SENT TO ITSELF
    # APPEND GPS LISTENER
    # canBus.targets.append([14, 8, 0])
    # canBus.targets.append([14, 8, 0])


def get_location():
    """
    Gets gps location from the CAN bus and returns it
    """
    location = (canBus.gpsLocation.latitude, canBus.gpsLocation.longtitude)
    return location


def get_distance_between(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two given GPS coordinates.
    """
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # calculate the result
    return c * 6371


def move_boat(x, y, rotation, power):
    """"
    Function used to perform general movement actions
    """
    canBus.sendMessage(a, b, c, d, e, canBus.moveCAN.generateData())
    # return true


def move_boat_to_coordinate(target_lat, target_lon):
    """
    Function used to move to a specific GPS coordinate. Has no innate collision detection.
    NOTE: REQUIRES TOLERANCE LEVEL FOR ADJUSTMENTS TO STOP
    """
    current_lat = canBus.gpsLocation.latitude
    current_lon = canBus.gpsLocation.longtitude

    # Repeat until boat is at target coordinates (within tolerance)
    while not (target_lat - TOLERANCE_DISTANCE < current_lat < target_lat + TOLERANCE_DISTANCE ) and \
            (target_lon - TOLERANCE_DISTANCE < current_lon < target_lon + TOLERANCE_DISTANCE):
        current_lat = canBus.gpsLocation.latitude
        current_lon = canBus.gpsLocation.longtitude

        # Calculate angle of travel from the X axis. Example: -45 being North-West and 135 being South-East
        travel_heading = math.degrees(math.atan2((current_lon - target_lon), (current_lat - target_lat)))
        align_heading(travel_heading)

        # Assumption is that every new command to the engines will be overwritten
        distance_to_target = get_distance_between(current_lat, current_lon, target_lat, target_lon)

        # Adjust power factor based on distance to target
        if distance_to_target > 20:
            power_scaling = 1
        elif distance_to_target > 10:
            power_scaling = 0.5
        elif distance_to_target > 5:
            power_scaling = 0.2
        else:
            power_scaling = 0.1

        move_boat(0, 1, 0, power_scaling)


def align_heading(target_heading=0.00):
    """
    Function used to hold the boat in a specific heading.
    NOTE: REQUIRES TOLERANCE LEVEL FOR ADJUSTMENTS TO STOP
    """
    # Get heading
    current_heading = 0

    # Repeat until boat is at target heading (within tolerance)
    while not (target_heading - TOLERANCE_ROTATIONAL < current_heading < target_heading + TOLERANCE_ROTATIONAL):
        if target_heading < 0:
            # move counter-clockwise
            move_boat(0, 0, -1, 0.1)
        elif target_heading > 0:
            # move clockwise
            move_boat(0, 0, -1, 0.1)

    # return true


def hold_position():
    """
    Function used to hold the boat in a specific location.
    """
    hold_lat = canBus.gpsLocation.latitude
    hold_lon = canBus.gpsLocation.longtitude
    move_boat_to_coordinate(hold_lat, hold_lon)

