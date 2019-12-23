from os import path

from AQNEXT.settings import PROJECT_ROOT
from YBAQNEXT.settings import INSTALLED_APPS
from YBWEB.ctxJSON import DICTJSON

YEBO_APPS = ()
CONTROLLER_APPS = ()
API_APPS = ()

rest = open(path.join(PROJECT_ROOT, "config/urls.json")).read()
oRest = DICTJSON.fromJSON(rest)

for app in oRest:
    if "controller" in oRest[app]:
        CONTROLLER_APPS += (app, )
    elif "api" in oRest[app]:
        API_APPS += (app, )
    else:
        YEBO_APPS += (app, )

INSTALLED_APPS += YEBO_APPS
INSTALLED_APPS += CONTROLLER_APPS
INSTALLED_APPS += API_APPS
# INSTALLED_APPS += ('channels', )