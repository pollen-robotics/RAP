#!/bin/bash
# Largely inspired by https://gitlab.inria.fr/dcaselli/rpi3-hotspot
# Merci Damien!

set -e

log() {
  echo "$1"
}


setup_hotspot() {
    log "Activating access point"

    if ! grep "^interface wlan0$" /etc/dhcpcd.conf; then
        log "Configure as static IP"
        sudo tee -a /etc/dhcpcd.conf > /dev/null <<EOT
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
EOT
        systemctl restart dhcpcd
    fi

    if [ "$(sysctl -n net.ipv4.ip_forward 2>/dev/null)" = "0" ]; then
        log "Update ip forwarding"
        sysctl -q -w net.ipv4.ip_forward=1
        sysctl -p
    fi

    log "Updating iptables"
    if ! iptables -t nat -C POSTROUTING -o eth0 -j MASQUERADE > /dev/null 2>&1; then
        iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    fi

    if ! iptables -C FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT > /dev/null 2>&1; then
        iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    fi

    if ! iptables -C FORWARD -i wlan0 -o eth0 -j ACCEPT > /dev/null 2>&1; then
        iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
    fi

    log "Restarting services"
    systemctl daemon-reload
    systemctl restart networking
    systemctl restart dnsmasq
    systemctl unmask hostapd
    systemctl enable hostapd
    systemctl restart hostapd

    log "Access point UP"
}

activate_wlan_dhcp() {
    log "Activating DHCP on WLAN"

    if [ "$(sysctl -n net.ipv4.ip_forward 2>/dev/null)" = "1" ]; then
        sysctl -q -w net.ipv4.ip_forward=0
        sysctl -p
    fi

    if iptables -t nat -C POSTROUTING -o eth0 -j MASQUERADE > /dev/null 2>&1; then
        iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
    fi

    if iptables -C FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT > /dev/null 2>&1; then
        iptables -D FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    fi

    if iptables -C FORWARD -i wlan0 -o eth0 -j ACCEPT > /dev/null 2>&1; then
        iptables -D FORWARD -i wlan0 -o eth0 -j ACCEPT
    fi

    systemctl stop dnsmasq
    systemctl stop hostapd
    systemctl disable hostapd
    systemctl mask hostapd

    if grep "^interface wlan0$" /etc/dhcpcd.conf; then
        sed -i "/interface wlan0/d" /etc/dhcpcd.conf
        sed -i "/    static ip_address=192.168.4.1\/24/d" /etc/dhcpcd.conf
        sed -i "/    nohook wpa_supplicant/d" /etc/dhcpcd.conf
        systemctl restart dhcpcd
    fi

    systemctl restart networking
}


run_hotspot_if_no_wifi() {
    activate_wlan_dhcp

    trial=0

    while [ $trial -lt  10 ]
    do
        sleep 5s

        log "Looking for Wifi..."
        if ifconfig wlan0 | grep -q inet; then
            log "Connected to WiFi!"
            return
        fi

        trial=$((trial+1))
    done

    log "No WiFi found!"
    setup_hotspot
}

run_hotspot_if_no_wifi
exit 0