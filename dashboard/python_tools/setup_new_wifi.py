import argparse
import sys
import re
import time

from subprocess import check_output, Popen, PIPE, call
from threading import Thread


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


def restart_raspberry(delay):
    def delay_reboot():
        time.sleep(delay)
        call(['sudo', 'reboot'])
    Thread(target=delay_reboot).start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add new wifi network to Reachy")
    parser.add_argument(
        "--ssid", help="id of the network"
        )
    parser.add_argument(
        "--password", help="wifi password"
        )
    args = parser.parse_args()

    setup_new_wifi(args.ssid, args.password)
    print("The WiFi network has been added.")
    print("The Raspberry will now restart to apply these changes.")

    restart_raspberry(2.0)
