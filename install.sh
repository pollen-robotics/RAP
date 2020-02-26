#!/bin/bash
# Largely inspired by https://gitlab.inria.fr/dcaselli/rpi3-hotspot
# Merci Damien!

set -e

apt update
apt install -y dnsmasq hostapd


if [ -f /etc/hostapd/hostapd.conf ]; then
  mv /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.old
fi
cp etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf

if [ -f /etc/default/hostapd ]; then
  mv /etc/default/hostapd /etc/default/hostapd.old
fi
cp etc/default/hostapd /etc/default/hostapd

if [ -f /etc/dnsmasq.conf ]; then
  mv /etc/dnsmasq.conf /etc/dnsmasq.conf.old
fi
cp etc/dnsmasq.conf /etc/dnsmasq.conf

cp etc/systemd/system/reachy-access-point.service /etc/systemd/system/reachy-access-point.service
cp usr/bin/reachy-access-point.sh /usr/bin/reachy-access-point
chmod +x /usr/bin/reachy-access-point

systemctl enable reachy-access-point.service

