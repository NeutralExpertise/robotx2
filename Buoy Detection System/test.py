import math
from math import radians, cos, sin, asin, sqrt

NORTHBOUND = 66
LON_METER = 0.000010812
LAT_METER = 0.00000901


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


def move_boat_by_distance(direction, distance, heading, gps):
    current_lat = gps[0]
    current_lon = gps[1]
    current_heading = heading
    print('MOVING AT HEADING: ' + str(heading))

    if direction == 'left':
        destination_lat = current_lat - (distance * cos(math.radians(current_heading + 90)) * LAT_METER)
        destination_lon = current_lon - (distance * sin(math.radians(current_heading + 90)) * LON_METER)
        print(destination_lat)
        print(destination_lon)
    elif direction == 'right':
        destination_lat = current_lat + (distance * cos(math.radians(current_heading + 90)) * LAT_METER)
        destination_lon = current_lon + (distance * sin(math.radians(current_heading + 90)) * LON_METER)
        print(destination_lat)
        print(destination_lon)

    new_gps = [destination_lat, destination_lon]

    return new_gps


def h_calc(current, modifier):
    new_heading = current + modifier
    if new_heading < 0:
        new_heading = 360 - abs(new_heading)

    return new_heading


def main():
    # print(get_distance_between(-33.72041106, 150.67072570, -33.72073454, 150.67152500))
    # print(5 * cos(math.radians(405)))
    # print(5 * sin(math.radians(405)))

    current_lat = -33.71990463
    current_lon = 150.67046285
    gps = [current_lat, current_lon]

    i_heading = 225

    print('point 1:')
    new_loc = move_boat_by_distance('right', 50, i_heading, gps)
    i_heading = h_calc(i_heading, 90)

    print('point 2:')
    new_loc = move_boat_by_distance('left', 100, i_heading, new_loc)
    i_heading = h_calc(i_heading, -90)

    print('point 3:')
    new_loc = move_boat_by_distance('left', 100, i_heading, new_loc)
    i_heading = h_calc(i_heading, -90)

    print('point 4:')
    new_loc = move_boat_by_distance('left', 100, i_heading, new_loc)
    i_heading = h_calc(i_heading, -90)

    print('point 5:')
    new_loc = move_boat_by_distance('left', 50, i_heading, new_loc)
    i_heading = h_calc(i_heading, -90)


if __name__ == '__main__':
    main()
