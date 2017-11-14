from postern.api import UI


class ActionHandler(UI.IExternalEventHandler):
    action_verb = None
    action_route = None
    action_data = None
    action_response = None

    def Execute(self, uiapp):
        axn_func = self.get_action(self.action_route)
        if axn_func:
            self.action_response = axn_func(uiapp, self.action_data)

    def GetName(self):
        return "HTTPExternalEventHandler"

    def get_action():
        pass
