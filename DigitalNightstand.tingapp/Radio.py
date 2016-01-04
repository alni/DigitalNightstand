import urllib
import os
import json
import base64

import Player
import config
from config import DIRBLE_API_KEY, USER_DATA_DIR

class Radio(object):
    """description of class"""

    @staticmethod
    def download_radio_channels(country_code="NO", count=30, replace=False):
        if DIRBLE_API_KEY is None:
            return None
        filename = USER_DATA_DIR + "/radio/" + country_code + ".json"
        if not os.path.exists(os.path.dirname(filename)):
            # If the folder path to the User Config Directory does not exists,
            # then create it + any non-existing parent folders
            os.makedirs(os.path.dirname(filename))
        if not os.path.exists(filename) or replace == True:
            url = "http://api.dirble.com/v2/countries/" + country_code + "/stations?"
            params = urllib.urlencode({
                # Base64 decode the API Key before sending it with the request
                "token": base64.b64decode(config.DIRBLE_API_KEY),
                "per_page": count
            })
            print url + params
            urllib.urlretrieve(url + params, filename)
        return filename

    @staticmethod
    def transform_downloaded_channels(country_code="NO"):
        radio_channels = []
        filename = USER_DATA_DIR + "/radio/" + country_code + ".json"
        if os.path.exists(filename):
            with open(filename) as data_file:
                radio_data = json.load(data_file)
            if not "channels" in radio_data:
                for channel in radio_data:
                    radio_channels.append({
                        "name": channel["name"],
                        "groups": [ country_code ],
                        "stream_uri": channel["streams"][0]["stream"]
                    })
                data = {"channels":radio_channels}
                with open(filename, "w") as outfile:
                    print os.path.abspath(outfile.name)
                    json.dump(data, outfile)

    def __init__(self, radio_channels=None, mplayer_path="D:/Personal/Downloads/Software/AudioVideo/MPlayer/MPlayer-x86_64-r37451+g531b0a3/mplayer.exe"):
        if radio_channels == None:
            radio_channels =  [
                ("NRK P1", "http://lyd.nrk.no/nrk_radio_p1_ostlandssendingen_mp3_h"),
                ("NRK P1+", "http://lyd.nrk.no/nrk_radio_p1pluss_mp3_h"),
                ("NRK P2", "http://lyd.nrk.no/nrk_radio_p2_mp3_h"),
                ("NRK P3", "http://lyd.nrk.no/nrk_radio_p3_mp3_h"),
                ("NRK P13", "http://lyd.nrk.no/nrk_radio_p13_mp3_h"),
                ("Alltid nyheter", "http://lyd.nrk.no/nrk_radio_alltid_nyheter_mp3_h"),
                ("Alltid RR", "http://lyd.nrk.no/nrk_radio_p3_radioresepsjonen_mp3_h"),
                ("Jazz", "http://lyd.nrk.no/nrk_radio_jazz_mp3_h"),
                ("Klassisk", "http://lyd.nrk.no/nrk_radio_klassisk_mp3_h"),
                ("Folkemusikk", "http://lyd.nrk.no/nrk_radio_folkemusikk_mp3_h"),
                ("mP3", "http://lyd.nrk.no/nrk_radio_mp3_mp3_h"),
                ("P3 Urort", "http://lyd.nrk.no/nrk_radio_p3_urort_mp3_h"),
                ("Sport", "http://lyd.nrk.no/nrk_radio_sport_mp3_h"),
                ("Sapmi", "http://lyd.nrk.no/nrk_radio_sami_mp3_h"),
                ("Super", "http://lyd.nrk.no/nrk_radio_super_mp3_h"),
                ("P1 Buskerud", "http://lyd.nrk.no/nrk_radio_p1_buskerud_mp3_h"),
                ("P1 Finnmark", "http://lyd.nrk.no/nrk_radio_p1_finnmark_mp3_h"),
                ("P1 Hedemark og Oppland", "http://lyd.nrk.no/nrk_radio_p1_hedmark_og_oppland_mp3_h"),
                ("P1 Hordaland", "http://lyd.nrk.no/nrk_radio_p1_hordaland_mp3_h"),
                ("P1 More og Romsdal", "http://lyd.nrk.no/nrk_radio_p1_more_og_romsdal_mp3_h"),
                ("P1 Nordland", "http://lyd.nrk.no/nrk_radio_p1_nordland_mp3_h"),
                ("P1 Oslo og Akershus", "http://lyd.nrk.no/nrk_radio_p1_ostlandssendingen_mp3_h"),
                ("P1 Rogaland", "http://lyd.nrk.no/nrk_radio_p1_rogaland_mp3_h"),
                ("P1 Sogn og Fjordane", "http://lyd.nrk.no/nrk_radio_p1_sogn_og_fjordane_mp3_h"),
                ("P1 Sorlandet", "http://lyd.nrk.no/nrk_radio_p1_sorlandet_mp3_h"),
                ("P1 Telemark", "http://lyd.nrk.no/nrk_radio_p1_telemark_mp3_h"),
                ("P1 Troms", "http://lyd.nrk.no/nrk_radio_p1_troms_mp3_h"),
                ("P1 Trondelag", " http://lyd.nrk.no/nrk_radio_p1_trondelag_mp3_h"),
                ("P1 Vestfold", "http://lyd.nrk.no/nrk_radio_p1_vestfold_mp3_h"),
                ("P1 Ostfold", "http://lyd.nrk.no/nrk_radio_p1_ostfold_mp3_h"),
            ]

        self.country_code = None
        self.radio_channels = radio_channels
        self.active_channel = 0
        self.player = Player.Player(
            self.radio_channels[self.active_channel]['stream_uri'], 
            ["-ss", "60"],
            mplayer_path)

    def next_channel(self):
        self.set_channel(self.active_channel + 1)
    
    def prev_channel(self):
        self.set_channel(self.active_channel - 1)

    def set_channel(self, index):
        if index == len(self.radio_channels):
            index = 0
        if index < 0:
            index = len(self.radio_channels) - 1
        self.active_channel = index
        print "Currently playing: " + self.radio_channels[self.active_channel]['name']
        self.player.load(
            self.radio_channels[self.active_channel]['stream_uri'],
             ["-ss", "60"]
        )

    def add_channel(self, display_name, channel, switch_to=False):
        self.radio_channels.append({
            'name': display_name,
            'stream_uri': channel
        })
        # self.radio_channels.append((display_name, channel))
        if switch_to:
            self.set_channel(-1)

    def get_active_channel(self):
        if self.active_channel < len(self.radio_channels):
            return self.radio_channels[self.active_channel]
        else:
            return {}

    def load_channels(self, filename):
        if filename is not None and os.path.exists(filename):
            with open(filename) as data_file:
                radio_data = json.load(data_file)
            self.radio_channels = radio_data["channels"]

    def change_country(self, country_code):
        filename = USER_DATA_DIR + "/radio/" + country_code + ".json"
        if self.country_code is None or self.country_code != country_code:
            self.country_code = country_code
            filename = Radio.download_radio_channels(country_code)
            Radio.transform_downloaded_channels(country_code)
            self.load_channels(filename)
            self.set_channel(0)
            return True
        else:
            self.load_channels(filename)
            return False


def test():
    radio_player = Radio()

    while 1:
        command = "" # raw_input("command\n")
        if command == "next":
            radio_player.next_channel()
        if command == "prev":
            radio_player.prev_channel()
        if command == "play" or command == "pause":
            radio_player.player.play_pause()
        if command == "stop":
            radio_player.player.stop()
        if command == "new":
            channel = raw_input("new radio channel").split(";")
            radio_player.add_channel(channel[0], channel[1])
            # radio_player.player.stop()
            # radio_player.player = Player(channel)
            # player.play()
        if command == "title":
            radio_player.player.get_info(None)
        if command == "exit":
            break
        radio_player.player.get_info(None)

if __name__ == '__main__':
    test()
