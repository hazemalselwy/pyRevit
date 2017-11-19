from postern import dotnet
from postern.api import DB, UI
from postern import rulemap
from postern import server


request = server.handler


class Postern(object):
    def __init__(self, appname):
        self.appname = appname
        rulemap.init_rulemap(appname)

    def add_url_rule(self, route_url, view_func, methods=['GET']):
        for method in methods:
            rulemap.set_rule(self.appname, route_url, method, view_func)

    def route(self, route_url, methods=['GET']):
        def decorator(f):
            self.add_url_rule(route_url, f, methods)
            return f
        return decorator

    def run(self):
        # FIXME: Make sure only a single server is running
        appserver = server.PosternServer()
        appserver.start()
