# Reachy Access Point

Turns the Reachy Raspberry-Pi as an access point when not connected to a WiFi. Mostly useful for configuring your WiFi on the robot without having to physically access it.

The code is largely inspired by [https://gitlab.inria.fr/dcaselli/rpi3-hotspot](https://gitlab.inria.fr/dcaselli/rpi3-hotspot) (Merci Damien !) and from [the official documentation](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md).

## How this works

An access point is created if no known WiFi is found.

Defaults AP parameters:
* ssid: "Reachy-AP" 
* passphrase: "Reachy-AP"

They can be changed by tweaking the [etc/hostapd/hostapd.conf file](./etc/hostapd/hostapd.conf).

Default static IP for the Raspberry-Pi: "192.168.4.1"

It can be changed in [systemd/system/reachy-access-point.sh](./systemd/system/reachy-access-point.sh).

## Dashboard

The dashboard can be accessed as a webserver hosted on the Raspberry-Pi. So, to access it:

* First, connect to the same network than the board (if you haven't configure your WiFi yet, you can connect to the Raspberry Hotspot Access Point "Reachy-AP")
* If you have Bonjour configured:
    * Go to http://raspberrypi.local/
* Otherwise use the board IP, on the Hotspot:
    * Go to http://192.168.4.1/


### Configure WiFi

* Connect on the Dashboard
* Go to WiFi Settings tab
* Add your WiFi config (SSID and passphrase)
* Reboot the Raspberry-Pi
* Re-connect on the dashboard on the setup WiFi


## Installation

* git clone https://github.com/pollen-robotics/RAB
* cd RAB
* sudo sh install.sh