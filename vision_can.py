# import can
import frc

class Vision_CAN:

    def __init__(self):
        can = frc.FrcCan('can0', 'socketcan')
        can.targets.append([16,8,0])






# Initialise CAN BUS
# Append listeners (including a listener to itself)
# Append Vision System Listener
# canBus.targets.append([])


# Identify gate
# Go to gate - Request to move forward
# Center - Request to move left or right
# Go forward - Request to move forward
# Identify black buoy
# Message that we are past gate
# Shutdown

# NAVIGATION ALIGNS WITH BLACK BUOY
       



# 1 and index 1 = start transmitting
# 1 and index 2 = stop transmitting

# Vision go to and through gate, know when centered, go foward, message the C2 that we are past the gates, C2 shuts down vision system, goes to navigation
# GPS used to move to point or hold

# CAN
# device 16
# 8
# movement = 3 (forward = 0, ) (4 values)
# direction (2 byte direction angle)
# speed (1 byte speed (signed)), 1 for full speed (full power = 100?), 0 for no speed