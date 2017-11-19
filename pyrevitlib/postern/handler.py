from postern.api import UI
from postern import rulemap


class RequestHandler(UI.IExternalEventHandler):
    appname = None
    route = None
    method = None
    data = None
    rcode = 200
    rdata = None

    def Execute(self, uiapp):
        rule_func = rulemap.get_rule(self.appname,
                                     self.route,
                                     self.method)
        if rule_func:
            try:
                self.rdata = rule_func(uiapp)
            except Exception as e:
                self.rcode = 500
                self.rdata = {"exception": str(e)}
        else:
            self.rcode = 404

    def GetName(self):
        return self.__class__.__name__
