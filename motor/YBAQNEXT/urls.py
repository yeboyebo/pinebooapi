import importlib
# from os import path
import os

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from YBUTILS.viewREST import routers
from YBWEB.ctxJSON import DICTJSON


def raiz(request):
    return ""


urlpatterns = []

for app in settings.CONTROLLER_APPS:
    controllerRouter = routers.controllerRouter(aplicacion=app)
    controllerRouter.registerDynamicModel(app)
    urlpatterns.append(path("{0}/".format(app), include(controllerRouter.urls))
    )


for app in settings.API_APPS:
    apiRouter = routers.apiRouter(aplicacion=app)
    apiRouter.registerDynamicModel(app)
    urlpatterns.append(path("{0}/".format(app), include(apiRouter.urls))
    )

# rootRouter = routers.rootRouter(aplicacion="")
# rootRouter.registerDynamicModel("")
# urlpatterns.append(path(r"^", include(rootRouter.urls))
# )

urlpatterns.append(path("admin/", admin.site.urls))
urlpatterns.append(path("", include("YBLOGIN.urls")))

urlpatterns.append(path("", raiz, name="root")
)



