import re
import sys

from subprocess import check_output, Popen, PIPE, CalledProcessError


def setup_new_wifi(ssid, password):
    config_file = '/etc/wpa_supplicant/wpa_supplicant.conf'

    # Generate psk using wpa_passphrase
    extra_config = check_output([
        'wpa_passphrase', ssid, password,
    ]).decode(sys.stdout.encoding)
    psk = re.search(r'\tpsk=(\w+)\n', extra_config).group(1)

    config = check_output([
        'sudo', 'cat', config_file,
    ]).decode(sys.stdout.encoding)

    if ssid in config:
        config = re.sub(r'\tpsk=(\w+)\n', f'\tpsk={psk}\n', config)
    else:
        config = f'{config}network={{\n\tssid="{ssid}"\n\tpsk={psk}\n}}\n'

    echo = Popen(['echo', config], stdout=PIPE)
    tee = Popen(['sudo', 'tee', config_file], stdin=echo.stdout)
    echo.wait()
    tee.wait()


def get_wlan_status():
    try:
        ssid = check_output(['iwgetid', '-r']).decode(sys.stdout.encoding).strip()
        mode = 'DHCP'
    except CalledProcessError:
        ssid = 'Reachy-AP'
        mode = 'Hotspot'

    return {
        'mode': mode,
        'SSID': ssid,
    }


if __name__ == '__main__':
    setup_new_wifi(
        ssid='pollen-demo',
        password='effetdemo',
    )
