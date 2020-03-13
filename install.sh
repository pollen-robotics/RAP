#!/bin/bash
# Largely inspired by https://gitlab.inria.fr/dcaselli/rpi3-hotspot
# Merci Damien!

set -e

apt update

#######################################
# Install, setup Access Point service #
#######################################

apt install -y dnsmasq hostapd

if [ -f /etc/hostapd/hostapd.conf ]; then
  mv /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.old
fi
cp scripts/etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf

if [ -f /etc/default/hostapd ]; then
  mv /etc/default/hostapd /etc/default/hostapd.old
fi
cp scripts/etc/default/hostapd /etc/default/hostapd

if [ -f /etc/dnsmasq.conf ]; then
  mv /etc/dnsmasq.conf /etc/dnsmasq.conf.old
fi
cp scripts/etc/dnsmasq.conf /etc/dnsmasq.conf

cp scripts/etc/systemd/system/reachy-access-point.service /etc/systemd/system/reachy-access-point.service
cp scripts/usr/bin/reachy-access-point.sh /usr/bin/reachy-access-point
chmod +x /usr/bin/reachy-access-point

systemctl enable reachy-access-point.service

###############################
# Install and setup Dashboard #
###############################

cp scripts/etc/systemd/system/reachy-dashboard.service /etc/systemd/system/reachy-dashboard.service
systemctl enable reachy-dashboard.service
