# SmokeControl
A Python program to plot temperatures from the Maverick ET-736 Digital Thermometer

!!! This is work in progress !!!

Unfortunately, the iChef iOS application for the ET-736 is the worst (cr)app.

That's why I decided to write my own, server based web-app.

.h2 (Planned) Features:

* Have multiple graphs displayed: short term and long term
* Have a simple timer (since start of cooking)
* .csv export
* Fan control (via raspberry pi shield)


.h2 Installation

.h3 Raspberry Pi

* Update Sources: sudo apt-get update
* Install dependencies: sudo apt-get install python3 git python3-pip
* Install setup tools:  sudo pip3 install --upgrade setuptools
* Install modules: pip3 install xmltodict matplotlib
* Download repository: git clone https://github.com/lsilberbauer/SmokeControl.git