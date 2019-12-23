"""
    Utilidades para el enrutamiento de acceso a multiples BBDD
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from django.db import connections
from django.conf import settings

from YBUTILS import mylogging as log

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
from django.utils.deprecation import MiddlewareMixin

milog = log.getLogger("YBUTILS.DbRouter")

# ----------------------------- VARIABLES GLOBALES
_CABECERA_YB_DB = "HTTP_X_YB_DB"

# -----------------------------MIDDLEWARE
_thread_locals = local()


class ThreadLocalMiddleware(MiddlewareMixin):
    """ Simple middleware that adds the request object in thread local storage. """

    def process_request(self, request):
        _thread_locals.request = request
        settings.SESSION_COOKIE_NAME = "sessionid" + request.META["SERVER_PORT"]

    def process_request_celery(self, request):
        _thread_locals.request = request
        settings.SESSION_COOKIE_NAME = "sessionid" + request["META"]["SERVER_PORT"]

    def process_response(self, request, response):
        if hasattr(_thread_locals, "request"):
            del _thread_locals.request
        return response


def fake_request():
    try:
        _thread_locals.request = local()
        _thread_locals.request.user = "auto"
        _thread_locals.request.session = {}
    except Exception as e:
        print(e)
        return False

    return True


def get_current_request():
    request = getattr(_thread_locals, "request", None)
    if request is None:
        fake_request()

    return getattr(_thread_locals, "request", None)


def get_current_user():
    request = get_current_request()
    if request:
        return getattr(request, "user", None)
    return None


def get_current_virtualenv():
    request = get_current_request()

    if request:
        meta = getattr(request, "META", None)
        if not meta:
            meta = request["META"]

        try:
            virtualEnv = meta["VIRTUAL_ENV"]
        except Exception:
            virtualEnv = getattr(meta, "VIRTUAL_ENV", None)

    return virtualEnv



# -----------------------------METODOS PARA OBTENER CONEXION
# USADO POR LEGACY
def dameConexionDef():
    """
    Metodo para obtener conexion defecto teniendo en cuenta que ha podido ser establecida a nivel de thread
    """
    micon = globalValues.getValue(_CABECERA_YB_DB, "default")
    return connections[micon]


# METODO ROUTER NORMAL
class DbRouterThread(MiddlewareMixin):
    """
    Retorna la guardada en thead o default
    """
    def db_for_read(self, model, **hints):
        milog.debug("SOLICITADA BASE DE DATOS LECTURA MODELO")
        aux = globalValues.getValue(_CABECERA_YB_DB, None)
        if aux is None:
            milog.info("No se ha detectado BBDD para el modelo")
        else:
            milog.debug("RESPONDIDA BBDD: %s", aux)
        return aux

    def db_for_write(self, model, **hints):
        milog.debug("SOLICITADA BASE DE DATOS ESCRITURA MODELO")
        aux = globalValues.getValue(_CABECERA_YB_DB, None)
        if aux is None:
            milog.info("No se ha detectado BBDD para el modelo")
        else:
            milog.debug("RESPONDIDA BBDD: %s", aux)
        return aux

        # if model._meta.app_label == "CGI":
        #     return "CGI"
        # return None
