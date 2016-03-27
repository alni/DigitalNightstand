import SimpleHTTPServer
import SocketServer
import logging
import cgi
import thread

import sys
import os
import posixpath
import urllib
import urllib2
import json
import base64
import inspect

import pygame
import tingbot

import config

api_data = {
    "radio": {
        "station": "(none)",
        "info": "(none)"
    }
}

alarm = None

# modify this to add additional routes
ROUTES = (
    # [url_prefix ,  directory_path]
    ['/media', '/var/www/media'],
    ['/icons', './res/icons/material-design-icons-2.0'],
    ['/tingbot', os.path.dirname(inspect.getfile(tingbot))],
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
            if self.path == "/api/get_fonts":
                self.api_call(data=pygame.font.get_fonts())
                return
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)
        if self.path == "/":
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            config.save_settings(data, config.CONFIG_FILE)
            config.SETTINGS = data
            if alarm is not None:
                alarm.set_settings(config.SETTINGS)

            logging.warning("\n")
            self.send_response(200)
            return
        elif self.path == "/forecastio_api_key":
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(data_string)
            config.save_settings(data, "weather/private.json")
            config.FORECASTIO_API_KEY = data["forecastio_api_key"]
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

def test():
    frontend = WebFrontend()
    frontend.serve()

    while 1:
        continue

if __name__ == '__main__':
    test()
