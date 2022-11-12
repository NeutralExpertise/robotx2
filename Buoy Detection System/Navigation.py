#!/usr/bin/python3

# File: Navigation.py
# Author: Jeremiah Ye
# EmailID: yeyjb001@mymail.unisa.edu.au

# Description:  This program contains the necessary movement commands to be used in the execution of Task 2.
#               It listens to the GPS module, the Nav Module (for heading), and itself on the CAN Bus.
#               Tolerance values (how close the program needs to run to its parameters) can be adjusted at the top.

import can
import frc
import math
from math import radians, cos, sin, asin, sqrt

GPS_METER = 0.00000900900900 # decimal degree equivalent of a meter
TOLERANCE_ROTATIONAL = 1  # in degrees
TOLERANCE_DISTANCE = 0.00001  # 2.22 meters
NORTHBOUND = 0



def initialise_can():
    global canBus
    canBus = frc.FrcCan('can0', 'socketcan')
    # GPS Listener
    canBus.targets.append([14, 8, 2])
    # Gate Movement Listener
    canBus.targets.append([20, 8, 1])
    # Nav Module Listener
    canBus.targets.append([20, 8, 2])


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

    # Return the result (in meters)
    return c * 6371 * 1000


def get_heading():
    """
    Gets current heading from the CAN bus and returns it
    """
    current_heading = canBus.movePosition.heading
    return current_heading


def move_boat(x, y, rotation, power):
    """"
    Function used to perform general movement actions
    """
    data = canBus.movePosition.generateCANData(x, y, rotation, power)
    canBus.sendMessageWithData(20, 8, 4, 0, 1, data)


def move_boat_to_coordinate(target_lat, target_lon):
    """
    Function used to move to a specific GPS coordinate. Has no innate collision detection.
    NOTE: REQUIRES TOLERANCE LEVEL FOR ADJUSTMENTS TO STOP
    """
    current_lat = canBus.gpsLocation.latitude
    current_lon = canBus.gpsLocation.longtitude

    # Repeat until boat is at target coordinates (within tolerance)
    while not (target_lat - TOLERANCE_DISTANCE < current_lat < target_lat + TOLERANCE_DISTANCE) and \
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


def move_boat_by_distance(direction, distance):
    current_lat = canBus.gpsLocation.latitude
    current_lon = canBus.gpsLocation.longtitude
    current_heading = get_heading()

    if (181 <= current_heading <= 359):
        # Facing Left - If you turn left, always + latitude
        # Turning right, always - latitude
        # North side meaning -latitude
        pass
    elif (1 <= current_heading <= 179):
        # Facing Right - If you turn left, always - latitude
        # Turning right, always + latitude
        # South side meanung + latitude
        pass
    elif current_heading == 0:
        # left = -lon, right = +lon
        if direction == -1:
            move_boat_to_coordinate(current_lat,current_lon - (distance * GPS_METER))
        elif direction == 1:
            move_boat_to_coordinate(current_lat, current_lon + (distance * GPS_METER))
    elif current_heading == 180:
        pass


def align_heading(target_heading=NORTHBOUND):
    """
    Function used to hold the boat in a specific heading.
    NOTE: REQUIRES TOLERANCE LEVEL FOR ADJUSTMENTS TO STOP
    """
    # Just a quirk of using atan2() - Degree is rendered positive till 180, then counts negatively backwards.
    if target_heading < 0:
        target_heading = 360 - abs(target_heading)
    # Get heading
    current_heading = get_heading()

    # Repeat until boat is at target heading (within tolerance)
    while not (target_heading - TOLERANCE_ROTATIONAL < current_heading < target_heading + TOLERANCE_ROTATIONAL):
        # Basic implementation that only turns boat clockwise
        move_boat(0, 0, 1, 0.1)


def hold_position():
    """
    Function used to hold the boat in a specific location.
    """
    hold_lat = canBus.gpsLocation.latitude
    hold_lon = canBus.gpsLocation.longtitude
    move_boat_to_coordinate(hold_lat, hold_lon)


def stop():
    """
    Stops all movement
    """
    # Need listener to function
    move_boat(0, 0, 0, 0)
