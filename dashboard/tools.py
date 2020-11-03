import re
import sys
import time

from subprocess import check_output, Popen, PIPE, CalledProcessError, call
from threading import Thread

from reachy.utils.discovery import discover_all

from git import Repo, cmd


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


def halt_raspberry(delay):
    def delay_halt():
        time.sleep(delay)
        call(['sudo', 'halt'])

    Thread(target=delay_halt).start()


def get_reachy_status():
    return {'status': discover_all()}


def update_git():
    local_repo = Repo('/home/pi/dev/reachy/software')
    latest_local_tag = str(local_repo.tags[-1])

    online_repo_info = cmd.Git().ls_remote('https://github.com/pollen-robotics/reachy')
    latest_online_tag = online_repo_info.split('tags/')[-1]
    if not latest_online_tag == latest_local_tag:
        cmd.Git('/Users/simon/dev/dummy_repo').pull()


def get_git_status():
    local_repo = Repo('/Users/simon/dev/dummy_repo')
    latest_local_tag = str(local_repo.tags[-1])

    online_repo_info = cmd.Git().ls_remote('https://github.com/pollen-robotics/reachy')
    latest_online_tag = online_repo_info.split('tags/')[-1]
  
    if not latest_online_tag == latest_local_tag:
        status = 'NOT_OK'
    else:
        status = 'OK'
    return status