import os
import json

from flask import Flask, request, redirect, url_for, render_template, Response

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


@app.route('/halt')
def halt():
    tools.halt_raspberry(delay=5)
    return render_template('halt.html')


@app.route('/api/reachy-status')
def update_status():
    return Response(
        response=json.dumps(tools.get_reachy_status()),
        mimetype='application/json',
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3972)
