#!/usr/bin/env python3


import urllib.request
import xmltodict
import time
import matplotlib.pyplot as plt
import mpld3
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Generate plot
        ax1.clear()
        ax1.plot(probe1_temps)
        ax1.plot(probe2_temps)

        # Send message back to client
        message = "<html><meta http-equiv='refresh' content='3'><head><title>ThermoGraph</title></head><body>\r\n"
        message += "<p>Probe 1: " + str(int(probe1_temps[len(probe1_temps) - 1])) + " &#8451</p>\r\n"
        message += "<p>Probe 2: " + str(int(probe2_temps[len(probe2_temps) - 1])) + " &#8451</p>\r\n"
        message += mpld3.fig_to_html(fig)
        message += "</html>"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5.0/9.0
    return celsius

def get_temperatures():
    while True:
        xmldata = urllib.request.urlopen("http://192.168.178.31/THERMO/history?max=1").read()
        parsedxml = xmltodict.parse(xmldata)

        temp1 = fahrenheit_to_celsius(int(parsedxml['temps']['probes']['Temp'][0]['@temp']))
        temp2 = fahrenheit_to_celsius(int(parsedxml['temps']['probes']['Temp'][1]['@temp']))

        print ("Temp1: " + str(temp1) + " Temp2: " + str(temp2))

        probe1_temps.append(temp1)
        probe2_temps.append(temp2)
        time.sleep(1)
    return

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
probe1_temps = []
probe2_temps = []

thread_get_temperatures = threading.Thread(target=get_temperatures)
thread_get_temperatures.start()

run()

