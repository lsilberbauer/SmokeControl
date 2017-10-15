#!/usr/bin/env python3

import urllib.request
import xmltodict
import time
import sys
import datetime
import csv    

def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5.0/9.0
    return celsius

if len(sys.argv) == 1:
    print("Usage: csv_writer.py name_of_log_file.csv")
    sys.exit(0)

csv_file_name = sys.argv[1]        
file_handle = open(csv_file_name, "a",newline='') 
writer = csv.writer(file_handle, delimiter=';')
print("File ", csv_file_name, " opened for writing")

while True:
    try:
        xmldata = urllib.request.urlopen("http://192.168.178.31/THERMO/history?max=1").read()
        parsedxml = xmltodict.parse(xmldata)

        temp1 = fahrenheit_to_celsius(int(parsedxml['temps']['probes']['Temp'][0]['@temp']))
        temp2 = fahrenheit_to_celsius(int(parsedxml['temps']['probes']['Temp'][1]['@temp']))

        print(str(datetime.datetime.now()) + " Temp1: " + str(temp1) + " Temp2: " + str(temp2))
        writer.writerow([datetime.datetime.now(), str(round(temp1,1)), str(round(temp2,1))])
        file_handle.flush()
        time.sleep(10)
    except KeyboardInterrupt:
        print("Keyboard Interuption received, quitting")
        break
    except TimeoutError:
        print("Timout Occured")
    #except:
    #    print("Unexpected error:", sys.exc_info()[0])

file_handle.close()


