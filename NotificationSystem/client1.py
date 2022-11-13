# File: clientTDN
# Author: Sitha Sinoun
# Email ID: sinsy077@mymail.unisa.edu.au

# Description: This program aims to act as a client for Technical Director's Network for use in the Maritime
#              Robotx Competition.  To function, the Technical DN will need to know the IP and port number of the
#              server it wants to connect to.  When connected the program will receive a NMEA like sentence Message.
#              What message received is determined by the task that the server program wishes to send,
#              it could be a Heartbeat message, an Entrance and Exit Gates Message or a message for another task.


import socket

# take the server name and port name
host = 'local host'
# port should match the server number
port = 5000

# create a socket at client side
# using TCP / IP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect it to server and port
# number on local computer.
s.connect(('192.168.1.4', port))  # NOTE: IP address should be the server it wants to connect to


# receive message string from
# server, at a time 1024 B
msg = s.recv(1024)

# repeat as long as message
# string are not empty

# receive data from the server and decoding to get the string
while msg:
    print(msg.decode())
    msg = s.recv(1024)

# close the connection
s.close()



