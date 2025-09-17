import logging
import os
import re
import pwnagotchi.plugins as plugins
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts

def clean_gps():
    #!/usr/bin/env python3
# Directory containing the files
    DATA_DIR = "/home/pi/handshakes"

# Regex to capture NAME and the rest of the filename
    pattern = re.compile(r"^(?P<name>[^_]+)_.+\.gps\.json$")

# Dictionary to track which NAME we've seen
    seen = {}

    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)

        # Only process files that match the pattern
        match = pattern.match(filename)
        if not match:
            continue

        name = match.group("name")

        if name not in seen:
            # Keep the first file we see for each NAME
            seen[name] = filepath
        else:
            # Delete duplicates
            logging.info(f"Removing duplicate GPS data for: {name}")
            os.remove(filepath)




class Example(plugins.Plugin):
    __author__ = 'evilsocket@gmail.com'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin for pwnagotchi that cleans up duplicate GPS files.'

    def __init__(self):
        logging.debug("example plugin created")
        self.options = dict()

    # called when http://<host>:<port>/plugins/<plugin>/ is called
    # must return a html page
    # IMPORTANT: If you use "POST"s, add a csrf-token (via csrf_token() and render_template_string)


    # called when the plugin is loaded
    def on_loaded(self):
        clean_gps()

    # called before the plugin is unloaded
    def on_unload(self, ui):
        pass

    # called when there's internet connectivity
    def on_internet_available(self, agent):
        pass

    # called to set up the ui elements
    def on_ui_setup(self, ui):
        pass

    # called when the ui is updated
    # called when the hardware display setup is done, display is an hardware specific object
    def on_display_setup(self, display):
        pass

    # called when everything is ready and the main loop is about to start
    def on_ready(self, agent):
        logging.info("unit is ready")
        # you can run custom bettercap commands if you want
        #   agent.run('ble.recon on')
        # or set a custom state
        #   agent.set_bored()

    # called when a non overlapping Wi-Fi channel is found to be free
    def on_free_channel(self, agent, channel):
        pass

    # called when the status is set to bored
    def on_bored(self, agent):
        pass

    # called when the status is set to sad
    def on_sad(self, agent):
        pass

    # called when the status is set to excited
    def on_excited(self, agent):
        pass

    # called when the status is set to lonely
    def on_lonely(self, agent):
        pass

    # called when the agent is rebooting the board
    def on_rebooting(self, agent):
        pass

    # called when the agent is waiting for t seconds
    def on_wait(self, agent, t):
        pass

    # called when the agent is sleeping for t seconds
    def on_sleep(self, agent, t):
        pass

    # called when the agent refreshed its access points list
    def on_wifi_update(self, agent, access_points):
        pass

    # called when the agent refreshed an unfiltered access point list
    # this list contains all access points that were detected BEFORE filtering
    def on_unfiltered_ap_list(self, agent, access_points):
        pass

    # called when the agent is sending an association frame
    def on_association(self, agent, access_point):
        clean_gps()

    # called when the agent is de-authenticating a client station from an AP
    def on_deauthentication(self, agent, access_point, client_station):
        clean_gps()

    # callend when the agent is tuning on a specific channel
    def on_channel_hop(self, agent, channel):
        pass

    # called when a new handshake is captured, access_point and client_station are json objects
    # if the agent could match the BSSID's to the current list, otherwise they are just the strings of the BSSIDs
    def on_handshake(self, agent, filename, access_point, client_station):
        clean_gps()

    # called when an epoch is over (where an epoch is a single loop of the main algorithm)
    def on_epoch(self, agent, epoch, epoch_data):
        clean_gps()

    # called when a new peer is detected
    def on_peer_detected(self, agent, peer):
        pass

    # called when a known peer is lost
    def on_peer_lost(self, agent, peer):
        pass
