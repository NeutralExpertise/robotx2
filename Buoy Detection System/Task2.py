# #import can
# #import GPS_MODULE
# #import VISION_SYSTEM
# #import HEARTBEAT_MONITOR

# class task_info:
#     def __init__(self):
#         self.gate_used = 0   

# def initialise_can():
#     global canBus
#     canBus = frc.FrcCan('can0', 'socketcan')

#     # Append all listeners
#     # APPEND SELF LISTENER (LISTENS TO MESSAGES SENT TO ITSELF
#     # APPEND GPS LISTENER
#     # canBus.targets.append([A, B, C])

# def main():
#     #Initialise can connection
#     initialise_can()

#     while True:
#         #LISTENING FOR CAN SIGNAL
#         #IF SIGNAL TO BEGIN TASK 2
#         print("Commencing Task 2")
#         task_2()
    
#         #IF SIGNAL TO COMPLETE COURSE
#         print("Commencing course exit")
#         exit_course()

# def task_2():
#     #ASSUMPTION: POSITIONED BETWEEN FIRST GATE
#     #STEP 1- MOVE TOWARDS FIRST GATE
#     #ACCESS VISION SYSTEM/GPS
#     #WHILE BOAT INCORRECT DISTANCE FROM GATE - GOTO 1
    
#     #STEP 2- ADJUST BOAT POSITION TO BE EQUIDISTANT FROM BUOYS
#     #ACCESS VISION SYSTEM/GPS
#     #WHILE BOAT IN INCORRECT POSITION, GOTO 2
    
#     #STEP 3- ACCESS VISION SYSTEM/GPS
#     #MOVE BOAT TILL BETWEEN BUOYS
#     #ACCESS BEACON SCANNER
#     #WHILE NO SIGNAL DETECTED, MOVE BOAT BACKWARDS AND SIDEWAYS TO NEXT GATE, THEN GOTO 3
    
#     #MOVE THROUGH GATE
#     #STEP 4- ACCESS VISION SYSTEM/GPS
#     #REPOSITION TO BLACK BUOY BASED ON GATE ENTERED
#     #WHILE BOAT IN INCORRECT POSITION, GOTO 4
    
#     #LOOP AROUND BUOY
#     #EXIT TO OTHER TASKS
    
# def exit_course():
#     #ASSUMPTION: BOAT GUIDED TO EXIT    
#     #STEP 1- ACCESS VISION SYSTEM/GPS
#     #RECALL GATE USED FROM TASK_INFO CLASS
#     #POSITION BOAT IN FRONT OF USED GATE
    
#     #STEP 2- ADJUST BOAT POSITION TO BE EQUIDISTANT FROM BUOYS
#     #ACCESS VISION SYSTEM/GPS
#     #WHILE BOAT IN INCORRECT POSITION, GOTO 2
    
#     #EXIT COURSE

# if __name__ == '__main__':
#     setup()
#     try:
#         main()
#     except KeyboardInterrupt:
#         destroy()