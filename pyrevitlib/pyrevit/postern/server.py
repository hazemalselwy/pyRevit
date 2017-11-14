
import argparse
import re
import cgi
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

from postern.api import UI
from postern import handler


# create the base action handler
# Revit external event handler that calls an action
# based on provided route
pevent = UI.ExternalEvent.Create(handler.ActionHandler())


class Resonse(object):
    pass


class ActionEventHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    if None != re.search('/api/v1/select/*', self.path):
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'application/json':
        length = int(self.headers.getheader('content-length'))
        data = json.loads(self.rfile.read(length))
        try:
            evt.target_view = 'select'
            evt.data = data['elements']
            pevent.Raise()
        except Exception as e:
            msg = str(e)
      else:
        data = {}
      self.send_response(200)
      self.send_header('Content-Type', 'application/txt')
      self.end_headers()
      self.wfile.write(msg)
    elif None != re.search('/api/v1/message/*', self.path):
      evt.target_view = 'msgbox'
      pevent.Raise()
      self.send_response(200)
      self.end_headers()
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return

  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    self.wfile.write('{"name":"ehsan"}')
    return


class ThreadedActionServer(ThreadingMixIn, HTTPServer):
  allow_reuse_address = True

  def shutdown(self):
    self.socket.close()
    HTTPServer.shutdown(self)


class ActionServer():
  def __init__(self, name=None, ip='', port=48884):
    self.server = ThreadedActionServer((ip, port), ActionEventHandler)

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
