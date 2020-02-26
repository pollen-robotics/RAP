# Reachy Access Point

Turns the Reachy Raspberry-Pi as an access point. Mostly useful for configuring your WiFi on the robot without having to physically access it.

The code is largely inspired by [https://gitlab.inria.fr/dcaselli/rpi3-hotspot](https://gitlab.inria.fr/dcaselli/rpi3-hotspot) (Merci Damien !) and from [the official documentation](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md).

## How this works

An access point is created if _/boot/hotspot_ file is present. If there is no such file, no access point will be set up and the _/etc/wpa_supplicant/wpa_supplicant.conf_ will be used.

Defaults AP parameters:
* ssid: "Reachy-AP" 
* passphrase: "Reachy-AP"

They can be changed by tweaking the [etc/hostapd/hostapd.conf file](./etc/hostapd/hostapd.conf).

Default static IP for the Raspberry-Pi: "192.168.4.1"

It can be changed in [systemd/system/reachy-access-point.sh](./systemd/system/reachy-access-point.sh).

## Installation

* git clone https://github.com/pollen-robotics/RAB
* cd RAB
* sudo sh install.sh