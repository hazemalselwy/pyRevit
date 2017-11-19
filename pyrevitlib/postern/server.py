import argparse
import re
import cgi
import json
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

from postern.api import UI
from postern import handler


# create the base Revit external event handler
# upon Raise(), finds and runs the appropriate func
handler = handler.RequestHandler()
pevent = UI.ExternalEvent.Create(handler)


class HttpRequestHandler(BaseHTTPRequestHandler):
    def parse_path(self):
        levels = self.path.split('/')
        if levels and len(levels) >= 2:
            appname = levels[1]
            if len(levels) > 2:
                route_levels = levels[2:]
                route = '/' + '/'.join(levels[2:])
            else:
                route = '/'

            return appname, route

        return None, None

    def process_request(self, method):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        # FIXME: correct process for various methods
        # e.g. GET does not have body
        if ctype == 'application/json':
            content = self.headers.getheader('content-length')
            try:
                appname, path = self.parse_path()
                if appname and path:
                    handler.appname = appname
                    handler.method = method
                    handler.route = path
                    handler.data = json.loads(self.rfile.read(int(content))) if content else None
                    pevent.Raise()
                    while pevent.IsPending:
                        pass
                    self.send_response(handler.rcode)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    if handler.rdata:
                        self.wfile.write(json.dumps(handler.rdata))
                    else:
                        self.wfile.write(json.dumps({}))
            except Exception as e:
              self.send_response(400)
              self.send_header('Content-Type', 'application/txt')
              self.end_headers()
              self.wfile.write(str(e))

    def do_GET(self):
        try:
            self.process_request(method='GET')
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/txt')
            self.end_headers()
            self.wfile.write(str(e))

    def do_POST(self):
        try:
            self.process_request(method='POST')
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/txt')
            self.end_headers()
            self.wfile.write(str(e))


class ThreadedHttpServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class PosternServer():
    def __init__(self, name=None, ip='', port=48889):
        self.server = ThreadedHttpServer((ip, port), HttpRequestHandler)
        self.start()

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def stop(self):
        self.server.shutdown()
        self.waitForThread()
