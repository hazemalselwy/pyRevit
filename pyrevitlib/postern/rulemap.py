from collections import namedtuple

from postern.dotnet import AppDomain


RULEMAP_KEY = 'posternViewFunctions'


Rule = namedtuple('Rule', ['url', 'verb'])


def init_root_rulemap():
    rootrulemap = {}
    AppDomain.CurrentDomain.SetData(RULEMAP_KEY, rootrulemap)
    return rootrulemap


def init_rulemap(appname=None):
    if appname:
        rootrulemap = get_rulemap()
        if not rootrulemap:
            rootrulemap = init_root_rulemap()

        rootrulemap[appname] = {}
    else:
        init_root_rulemap()


def get_rulemap(appname=None):
    rootrulemap = AppDomain.CurrentDomain.GetData(RULEMAP_KEY)
    if appname:
        if rootrulemap:
            return rootrulemap.get(appname, None)
    else:
        return rootrulemap


def set_rule(appname, route, method, viewfunc):
    rule = Rule(url=route, verb=method)
    apprulemap = get_rulemap(appname)
    if apprulemap is not None:
        apprulemap[rule] = viewfunc
        return True


def get_rule(appname, route, method):
    rule = Rule(url=route, verb=method)
    apprulemap = get_rulemap(appname)
    if apprulemap:
        return apprulemap.get(rule, None)


def get_rullmap(appname=None):
    return get_rulemap(appname)
