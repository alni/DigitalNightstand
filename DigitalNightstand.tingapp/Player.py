import time
import subprocess
import re

class Player(object):
    """
    Player class used to initialize and provide control of MPlayer
    """
    def __init__(self, stream, params=None, mplayer_path="D:/Personal/Downloads/Software/AudioVideo/MPlayer/MPlayer-x86_64-r37451+g531b0a3/mplayer.exe"):
        """
        Initialize the Player with stream.

        Parameters:
        - stream : the stream to pass to MPlayer
        - params : (optional) pass extra arguments to the MPlayer subproccess
        - mplayer_path : (optional) the path to the MPlayer executable
        """
        print stream
        self.info = None
        self.title = None
        self.name = None
        self.mplayer_path = mplayer_path
        self.player = self._create_player(stream, params, mplayer_path)

    def _create_player(self, stream, params, mplayer_path):
        args = [mplayer_path, "-slave", "-quiet", "-cache", "1024"]
        if params is not None:
            args.extend(params)
        if stream.endswith(".m3u") or stream.endswith(".pls"):
            args.append("-playlist")
        args.append(stream)
        self.player = subprocess.Popen(args, 
                                       stdin=subprocess.PIPE, 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.STDOUT,
                                       bufsize = 1, universal_newlines = True)
        return self.player

    def play_pause(self):
        self.player.stdin.write("pause\n")
        self.player.stdin.flush()

    def stop(self):
        self.player.stdin.write("quit\n")
        self.player.stdin.flush()
        self.player.kill()

    def vol_down(self):
        self.player.stdin.write("volume -1\n")
        self.player.stdin.flush()

    def vol_up(self):
        self.player.stdin.write("volume 1\n")
        self.player.stdin.flush()

    def toggle_mute(self):
        self.player.stdin.write("mute\n")
        self.player.stdin.flush()

    def mute(self):
        self.player.stdin.write("mute 1\n")
        self.player.stdin.flush()

    def unmute(self):
        self.player.stdin.write("mute 0\n")
        self.player.stdin.flush()

    def seek(self, sec=120):
        self.player.stdin.write("seek %d\n" % sec)
        self.player.stdin.flush()

    def load(self, stream, params=None):
        command = "loadfile " + stream + "\n"
        self.name = None
        self.info = None
        self.player.kill()
        self.player = self._create_player(stream, params, self.mplayer_path)

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

    def set_title(self):
        str = u'(none)'
        attrs = None
        # line = self.player.stdout.readline()
        for line in iter(self.player.stdout.readline, ''):
            # print line
            if line.startswith('ICY Info: StreamTitle='):
                title = line.split("ICY Info: StreamTitle=")[1].strip()
                if title is not None:
                    self.title = title[1:-2]
                print '\nStream title: '+self.title

    def get_info(self, attr="StreamTitle"):
        str = u'(none)'
        attrs = None
        # line = self.player.stdout.readline()
        for line in iter(self.player.stdout.readline, ''):
            print line
            if line.startswith('ICY Info:'):
                info = line.split(':', 1)[1].strip()
                attrs = dict(re.findall("(\w+)='([^']*)'", info))
                # print 'Stream title: '+attrs.get('StreamTitle', '(none)')
                if attrs is not None and attrs.has_key(attr):
                    self.info = attrs
            if self.info is not None:
                str = self.info.get(attr, '(none)')
            # print '\nStream title: '+str
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

