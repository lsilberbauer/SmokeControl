#!/usr/bin/env python3


import time
import matplotlib.pyplot as plt
import mpld3
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import datetime
import csv


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        #try:
        #get csv data
        csv_file_name = sys.argv[1]
        file_handle = open(csv_file_name, "r")
        reader = csv.reader(file_handle, delimiter=';')
        
        timestamps = []
        probe1_temps = []
        probe2_temps = []
        
        for row in reader:     
            timestamps.append(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f"))
            probe1_temps.append(row[1])
            probe2_temps.append(row[2])                        
            
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Generate plot        
        ax1.clear()    
        ax1.plot(timestamps, probe1_temps)
        ax1.plot(timestamps, probe2_temps)

        # Send message back to client
        message = "<html><meta http-equiv='refresh' content='5'><head><title>ThermoGraph</title></head><body>\r\n"
        message += "<p>Probe 1: " + str(float(probe1_temps[len(probe1_temps) - 1])) + " &#8451</p>\r\n"
        message += "<p>Probe 2: " + str(float(probe2_temps[len(probe2_temps) - 1])) + " &#8451</p>\r\n"
        message += "<p>Last Update " + str(int((datetime.datetime.now() - timestamps[len(timestamps) -1]).total_seconds())) +" seconds ago</p>"
        message += mpld3.fig_to_html(fig)
        message += "</html>"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        #except:
        #    print("Unexpected error:", sys.exc_info()[0])
        return

def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()
    
if len(sys.argv) == 1:
    print("Usage: webserver.py name_of_log_file.csv")
    sys.exit(0)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

run()

