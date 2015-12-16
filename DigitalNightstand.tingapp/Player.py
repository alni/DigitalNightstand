import time
import subprocess
import re

class Player(object):
    """description of class"""
    def __init__(self, channel, mplayer_path="D:/Personal/Downloads/Software/AudioVideo/MPlayer/MPlayer-x86_64-r37451+g531b0a3/mplayer.exe"):
        print channel
        self.info = None
        self.name = None
        self.mplayer_path = mplayer_path
        self.player = self._create_player(channel, mplayer_path)

    def _create_player(self, channel, mplayer_path):
        self.player = subprocess.Popen([mplayer_path, "-slave", "-quiet", "-cache", "1024", channel], 
                                       stdin=subprocess.PIPE, 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.STDOUT,
                                       bufsize = 1, universal_newlines = True)
        return self.player

    def play_pause(self):
        self.player.stdin.write("pause\n")

    def stop(self):
        self.player.stdin.write("quit\n")

    def vol_down(self):
        self.player.stdin.write("volume -1\n")

    def vol_up(self):
        self.player.stdin.write("volume 1\n")

    def mute(self):
        self.player.stdin.write("mute\n")

    def load(self, channel):
        command = "loadfile " + channel + "\n"
        self.name = None
        self.info = None
        self.player.kill()
        self.player = self._create_player(channel, self.mplayer_path)

    def set_name(self):
        not_found = True
        while not_found:
            line = self.player.stdout.readline().rstrip()
            # print line + "\n"
            if self.name == None or line != '':
                if line.startswith("Name   :"):
                    name = line.split(":", 1)[1].strip()
                    self.name = name + ""
                    break
            else:
                break


    def get_name(self):
        return self.name

    def get_info(self, attr="StreamTitle"):
        str = u'(none)'
        line = self.player.stdout.readline()
        # for line in self.player.stdout:
        # print line
        if line.startswith('ICY Info:'):
            info = line.split(':', 1)[1].strip()
            attrs = dict(re.findall("(\w+)='([^']*)'", info))
            # print 'Stream title: '+attrs.get('StreamTitle', '(none)')
            self.info = attrs
        if self.info is not None:
            str = self.info.get(attr, '(none)')
        print '\nStream title: '+str
        return str 

# player = Player("http://http-live.sr.se/p1-mp3-192")

while 0:
    command = raw_input("command\n")
    if command == "vol_down":
        player.vol_down()
    if command == "vol_up":
        player.vol_up()
    if command == "mute":
        player.mute()
    if command == "play" or command == "pause":
        player.play_pause()
    if command == "stop":
        player.stop()
    if command == "name":
        player.set_name()
        print player.get_name()
    if command == "new":
        channel = raw_input("new radio channel")
        player.stop()
        player.load(channel)
        # player = Player(channel)
        # player.play()
    if command == "exit":
        break

