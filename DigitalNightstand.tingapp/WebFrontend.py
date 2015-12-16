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

from appdirs import AppDirs

dirs = AppDirs("DigitalNightstand.tingapp", "Alexander Nilsen")

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
    
    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        if self.path == "/api/":
            #send code 200 response
            self.send_response(200)
 
            #send header first
            self.send_header('Content-type','application/json')
            self.end_headers()

            #send content to client
            self.wfile.write(json.dumps(api_data))
            return
        if self.path == "/api/play":
            if radio is not None:
                #send code 200 response
                self.send_response(200)
                radio.player.play_pause()
                #send header first
                self.send_header('Content-type','application/json')
                self.end_headers()

                #send content to client
                self.wfile.write(json.dumps(api_data))
                return
            else:
                self.send_error(501, "Radio not set to an instance")
                return
        if self.path == "/api/pause":
            if radio is not None:
                #send code 200 response
                self.send_response(200)
                radio.player.play_pause()
                #send header first
                self.send_header('Content-type','application/json')
                self.end_headers()

                #send content to client
                self.wfile.write(json.dumps(api_data))
                return
            else:
                self.send_error(501, "Radio not set to an instance")
                return
        if self.path == "/api/prev":
            if radio is not None:
                #send code 200 response
                self.send_response(200)
                radio.prev_channel()
                #send header first
                self.send_header('Content-type','application/json')
                self.end_headers()

                #send content to client
                self.wfile.write(json.dumps(api_data))
                return
            else:
                self.send_error(501, "Radio not set to an instance")
                return
        if self.path == "/api/next":
            if radio is not None:
                #send code 200 response
                self.send_response(200)
                radio.next_channel()
                #send header first
                self.send_header('Content-type','application/json')
                self.end_headers()

                #send content to client
                self.wfile.write(json.dumps(api_data))
                return
            else:
                self.send_error(501, "Radio not set to an instance")
                return
        if self.path == "/api/vol_down":
            if radio is not None:
                #send code 200 response
                self.send_response(200)
                radio.player.vol_down()
                #send header first
                self.send_header('Content-type','application/json')
                self.end_headers()

                #send content to client
                self.wfile.write(json.dumps(api_data))
                return
            else:
                self.send_error(501, "Radio not set to an instance")
                return
        if self.path == "/api/vol_up":
            if radio is not None:
                #send code 200 response
                self.send_response(200)
                radio.player.vol_up()
                #send header first
                self.send_header('Content-type','application/json')
                self.end_headers()

                #send content to client
                self.wfile.write(json.dumps(api_data))
                return
            else:
                self.send_error(501, "Radio not set to an instance")
                return
        if self.path == "/api/vol_mute":
            if radio is not None:
                #send code 200 response
                self.send_response(200)
                radio.player.mute()
                #send header first
                self.send_header('Content-type','application/json')
                self.end_headers()

                #send content to client
                self.wfile.write(json.dumps(api_data))
                return
            else:
                self.send_error(501, "Radio not set to an instance")
                return
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        with open("test123456.json", "w") as outfile:
            print os.path.abspath(outfile.name)
            json.dump(data, outfile)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        logging.warning("======= POST VALUES =======")
        print form.getvalue("alarm_01_days")
        for item in form.list:
            logging.warning(item)
        logging.warning("\n")
        
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
