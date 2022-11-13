import socketserver

class EchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo back to the client
        data = self.request.recv(1024)
        self.request.send(data)
        return


if __name__ == '__main__':

    import socket
    import threading
    import geocoder
    import time
    from datetime import datetime
    from pytz import timezone

    while 1:

        myloc = geocoder.ip("me")
        para_long = str(myloc.latlng[1])
        para_lat = str(myloc.latlng[0])

        aedt_tz = timezone('Australia/Sydney')
        datetime.now(aedt_tz)

        count = 0
        message_id = "$RXHRB"
        latitude = para_lat
        north_south_indicator = "N"
        longitude = para_long
        east_west_indicator = "W"
        team_id = "ROBOT"
        system_mode = str(2)
        uav_status = str(1) + "*"
        checksum = str(11)

        address = ('localhost', 0) # let the kernel give us a port
        server = socketserver.TCPServer(address, EchoRequestHandler)
        ip, port = server.server_address # find out what port we were given

        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True) # don't hang on exit
        t.start()

        # Connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))

        current_datetime = datetime.now(aedt_tz)
        current_day = str(current_datetime)[8:10]
        current_month = str(current_datetime.month)
        current_year = str(current_datetime.year)[2:4]

        sydney_hour = str(current_datetime)[11:13]
        sydney_minute = str(current_datetime)[14:16]
        sydney_second = str(current_datetime)[17:19]

        aedt_date = current_day + current_month + current_year
        aedt_time = sydney_hour + sydney_minute + sydney_second

        # Send the data
        message = ("Heartbeat Message = " + message_id + "," + aedt_date + "," + aedt_time + "," + latitude + "," + north_south_indicator
        + "," + longitude + "," + east_west_indicator + "," + team_id + "," + system_mode + "," + uav_status + checksum).encode()
        time.sleep(1)

        print('Sending : "%s"' % message)
        len_sent = s.send(message)

        # Receive a response
        response = s.recv(len_sent)
        print('Received: "%s"' % response)

# Clean up
s.close()
server.socket.close()