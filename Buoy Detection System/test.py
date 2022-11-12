import math
from math import radians, cos, sin, asin, sqrt

NORTHBOUND = 66
GPS_METER = 0.000010812

def navigation():
    print(NORTHBOUND)


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
    return c * 6371 * 1000

def move_boat_by_distance(direction, distance):
    current_lat = -33.72063750
    current_lon = 150.67162183
    current_heading = 90

    destination_lat = current_lat + (distance * cos(math.radians(current_heading + 90)) * GPS_METER)
    destination_lon = current_lon + (distance * sin(math.radians(current_heading + 90)) * GPS_METER)
    print(destination_lat)
    print(destination_lon)

def main():
    # print(get_distance_between(-33.72041106, 150.67072570, -33.72073454, 150.67152500))
    # print(5 * cos(math.radians(405)))
    # print(5 * sin(math.radians(405)))

    move_boat_by_distance('right', 100)


if __name__ == '__main__':
    main()
