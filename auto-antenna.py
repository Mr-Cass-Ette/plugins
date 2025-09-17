import pwnagotchi.plugins as plugins
import pwnagotchi
import logging
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import subprocess
import time
import os
import json
from pathlib import Path





class ext_wifi(plugins.Plugin):
    __author__ = 'chris@holycityhosting.com'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Activates external wifi adapter'

    def __init__(self):
        self.ready = 0
        self.status = ''
        self.network = ''
        self.change = False
        self.CONFIG_FILE = Path("persistant_memory.json")

    def on_ui_setup(self, ui):
        # add custom UI elements
        ui.add_element('antenna', LabeledValue(color=BLACK, label='iface:', value='wlan0', position=(ui.width() / 2 - 25, 0),
                                           label_font=fonts.Bold, text_font=fonts.Medium))
        

    def _read_status(self):
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, "r") as f:
                data = json.load(f)
            return data.get("status")
        self._write_status("wlan0")
        return "wlan0"

    def _write_status(self, value):
        data = {}
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, "r") as f:
                data = json.load(f)
        data["status"] = value
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)


    def on_loaded(self):
        _log("plugin loaded")
        self.ready = 1
        #mode = self.options['mode']
        interface = "wlan1"


        if (os.path.exists("/sys/class/net/wlan1")):
            _log("External adapter present")
            self._write_status("wlan1")
        else:
            _log("Internal adapter present")
            self._write_status("wlan0")

    def on_ui_update(self, ui):
        ui.set('antenna', self._read_status())
        
    def on_epoch(self, agent, epoch, epoch_data):
        if (os.path.exists("/sys/class/net/wlan1") and self._read_status() != "wlan1"):
            subprocess.run('sed -i s/mon0/{interface}/g /usr/bin/bettercap-launcher'.format(interface=interface), shell=True).stdout
            subprocess.run('sed -i s/mon0/{interface}/g /usr/local/share/bettercap/caplets/pwnagotchi-auto.cap'.format(interface=interface), shell=True).stdout
            subprocess.run('sed -i s/mon0/{interface}/g /usr/local/share/bettercap/caplets/pwnagotchi-manual.cap'.format(interface=interface), shell=True).stdout
            subprocess.run('sed -i s/mon0/{interface}/g /etc/pwnagotchi/config.toml'.format(interface=interface), shell=True).stdout
            subprocess.run('sed -i s/mon0/{interface}/g /usr/bin/pwnlib'.format(interface=interface), shell=True).stdout
            _log("External adapter activated")
            self._write_status("wlan1")
            os.system("sudo reboot")
        elif (os.path.exists("/sys/class/net/wlan0") and self._read_status() != "wlan0"):
            subprocess.run('sed -i s/{interface}/mon0/g /usr/bin/bettercap-launcher'.format(interface=interface), shell=True).stdout
            subprocess.run('sed -i s/{interface}/mon0/g /usr/local/share/bettercap/caplets/pwnagotchi-auto.cap'.format(interface=interface), shell=True).stdout
            subprocess.run('sed -i s/{interface}/mon0/g /usr/local/share/bettercap/caplets/pwnagotchi-manual.cap'.format(interface=interface), shell=True).stdout
            subprocess.run('sed -i s/{interface}/mon0/g /etc/pwnagotchi/config.toml'.format(interface=interface), shell=True).stdout
            subprocess.run('sed -i s/{interface}/mon0/g /usr/bin/pwnlib'.format(interface=interface), shell=True).stdout
            _log("Internal adapter activated")
            self._write_status("wlan0")
            os.system("sudo reboot")

def _run(cmd):
    result = subprocess.run(cmd, shell=True, stdin=None, stderr=None, stdout=subprocess.PIPE, executable="/bin/bash")
    return result.stdout.decode('utf-8').strip()

def _log(message):
    logging.info('[ext_wifi] %s' % message)