import SimpleHTTPServer
import SocketServer
import logging
import cgi
import thread

import sys
import os
import posixpath
import urllib
import json

import config

api_data = {
    "radio": {
        "station": "(none)",
        "info": "(none)"
    }
}

radio = None

# modify this to add additional routes
ROUTES = (
    # [url_prefix ,  directory_path]
    ['/media', '/var/www/media'],
    ['/icons', './res/icons/material-design-icons-2.0'],
    ['',       './www_data']  # empty string for the 'default' match
)

class _ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def translate_path(self, path):
        """translate path given routes"""

        # set default root to cwd
        root = os.getcwd()
        
        # look up routes and set root directory accordingly
        for pattern, rootdir in ROUTES:
            if path.startswith(pattern):
                # found match!
                path = path[len(pattern):]  # consume path up to pattern len
                root = rootdir
                break
        
        # normalize path and prepend root directory
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        
        path = root
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)

        return path

    def api_call(self, method=None, data=None):
        #send code 200 response
        self.send_response(200)
        if method is not None:
            method()
        #send header first
        self.send_header('Content-type','application/json')
        self.end_headers()
        if data is None:
            data = api_data
        #send content to client
        self.wfile.write(json.dumps(data))
    
    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        if self.path == "/api/":
            self.api_call()
            return
        if self.path.startswith("/api/"):
            if self.path == "/api/config":
                self.api_call(data=config.SETTINGS)
                return
            if radio is not None:
                if self.path == "/api/play":
                    self.api_call(radio.player.play_pause)
                    return
                if self.path == "/api/pause":
                    self.api_call(radio.player.play_pause)
                    return
                if self.path == "/api/prev":
                    self.api_call(radio.prev_channel)
                    return
                if self.path == "/api/next":
                    self.api_call(radio.next_channel)
                    return
                if self.path == "/api/vol_down":
                    self.api_call(radio.player.vol_down)
                    return
                if self.path == "/api/vol_up":
                    self.api_call(radio.player.vol_up)
                    return
                if self.path == "/api/vol_mute":
                    self.api_call(radio.player.mute)
                    return
                if self.path.startswith("/api/change_country/"):
                    country_code = self.path.split("/")[-1]
                    filename = radio.download_radio_channels(country_code)
                    radio.transform_downloaded_channels(country_code)
                    radio.load_channels(filename)
                    self.api_call()
                    return
            else:
                self.send_error(501, "Radio not set to an instance")
                return
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)
        if self.path == "/":
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            config.save_settings(data, config.CONFIG_FILE)
            logging.warning("\n")
            self.send_response(200)
            return
        elif self.path == "/dirble_api_key":
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(data_string)
            config.save_settings(data, "radio/private.json")
            config.DIRBLE_API_KEY = data["dirble_api_key"]
            logging.warning("\n")
            self.send_response(200)
            return
        else:
            self.send_error(501, "POST request is not supported with path")
            return
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

class WebFrontend(object):
    """description of class"""
    def __init__(self, ip_address="", port=8000):
        self.handler = _ServerHandler
        self.server = SocketServer.TCPServer((ip_address, port), self.handler)

    def serve(self):
        thread.start_new_thread(self.server.serve_forever, ())

    def stop(self):
        self.server.shutdown()


# frontend = WebFrontend()
# frontend.serve()

while 0:
    continue
