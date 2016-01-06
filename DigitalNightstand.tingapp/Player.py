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
        - params : (optional) pass extra arguments to the MPlayer subprocess
        - mplayer_path : (optional) the path to the MPlayer executable
        """
        print stream
        self.info = None
        self.title = None
        self.name = None
        self.mplayer_path = mplayer_path
        self.player = self._create_player(stream, params, mplayer_path)

    def _create_player(self, stream, params, mplayer_path):
        if stream is not None:
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
        else:
            self.player = None
        return self.player

    def _send_command(self, command):
        if self.player:
            self.player.stdin.write(command + "\n")
            try:
                self.player.stdin.flush()
            finally:
                return

    def play_pause(self):
        """Toggle Play/Pause"""
        self._send_command("pause")

    def stop(self):
        """Stop, quit and kill the player"""
        self._send_command("quit")
        if self.player:
            self.player.kill()

    def vol_down(self):
        """Decrease the volume"""
        self._send_command("volume -1")

    def vol_up(self):
        """Increase the volume"""
        self._send_command("volume 1")

    def toggle_mute(self):
        """Toggle Mute"""
        self._send_command("mute")

    def mute(self):
        """Mute"""
        self._send_command("mute 1")

    def unmute(self):
        """Unmute"""
        self._send_command("mute 0")

    def seek(self, sec=120):
        """Seek the playback of the given seconds"""
        self._send_command("seek %d" % sec)

    def load(self, stream, params=None):
        """Load new stream with optional additional MPlayer parameters"""
        command = "loadfile " + stream + "\n"
        self.name = None
        self.info = None
        if self.player:
            self.player.kill()
        self.player = self._create_player(stream, params, self.mplayer_path)

    def set_name(self):
        """Sets the name parsed from the MPlayer output"""
        if self.player is None:
            return
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
        """Returns the name parsed from the MPlayer output"""
        return self.name

    def set_title(self):
        """Set the title parsed from the MPlayer output"""
        if self.player is None:
            return
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
        """Gets and set the info parsed from the MPlayer output"""
        if self.player is None:
            return
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

def test():
    player = Player("http://http-live.sr.se/p1-mp3-192")

    while 1:
        command = raw_input("command\n")
        if command == "vol_down":
            player.vol_down()
        if command == "vol_up":
            player.vol_up()
        if command == "mute":
            player.toggle_mute()
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

if __name__ == '__main__':
    test()
