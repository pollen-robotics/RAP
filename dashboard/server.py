import os

from flask import Flask, request, redirect, url_for, render_template

import tools

app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)

notifications = []


@app.route('/update-wifi', methods=['POST'])
def update_wifi():
    tools.setup_new_wifi(request.form['ssid'], request.form['password'])

    notifications.append({
        'level': 'warning',
        'message': 'Config updated! Please reboot the Raspberry for the change to be taken into account.',
    })

    return redirect(url_for('wifi'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wifi')
def wifi():
    wlan_config = tools.get_wlan_status()

    status = {}

    if wlan_config['mode'] == 'DHCP':
        status['level'] = 'success'
        status['icon'] = 'wifi'
        status['title'] = 'WiFi'
        status['message'] = 'Connected'

    else:
        status['level'] = 'warning'
        status['icon'] = 'wifi_tethering'
        status['title'] = 'Hotspot'
        status['warning'] = True
        status['message'] = 'No WiFi found...'

    status['SSID'] = wlan_config['SSID']

    return render_template(
        'wifi.html',
        notifications=notifications,
        status=status,
    )
