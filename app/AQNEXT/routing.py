# from channels.routing import route
# from YBUTILS.wsConsumers import *

from channels.routing import ProtocolTypeRouter
from django.urls import path
from django.urls import re_path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from YBUTILS.wsConsumers import MyConsumer, ChatConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path(r"algo/", MyConsumer),
            re_path(r'ws/chat/(?P<room_name>\w+)/$', MyConsumer)
        ]),
    ),
})

from .local import *
from pineboolib import application as pineboolib_app
from YBUTILS.DbRouter import get_current_user
from pineboolib.loader.projectconfig import ProjectConfig
from pineboolib.core.settings import CONFIG
from pineboolib.loader import main
from pineboolib.application.parsers import parser_qsa as qsaparser
#from pineboolib.application.parsers import qsaparser
from pineboolib.application.utils import path
qsaparser.USE_THREADS = False


def nombre_session():
    return get_current_user()


pineboolib_app.PROJECT.set_session_function(nombre_session)
print("_________________")
print(DATABASES)
SQL_CONN = ProjectConfig(database=DATABASES["default"]["NAME"], host=DATABASES["default"]["HOST"], port=DATABASES["default"]["PORT"], type="PostgreSQL (PSYCOPG2)", username=DATABASES["default"]["USER"], password=DATABASES["default"]["PASSWORD"])
if StaticLoader:
    CONFIG.set_value("StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), True)  # Para activar carga estática
    CONFIG.set_value("StaticLoader/%s/dirs" % DATABASES["default"]["NAME"], dirs)  # Directorios para carga estatica(Configurar en local.py, Ej: dirs = [True, "/home/modulos/api/scripts", True, "/home/modulos/libreria/scripts"])
    CONFIG.set_value("ebcomportamiento/SLConsola", True)   # Muestra debug por consola
    CONFIG.set_value("application/dbadmin_enabled", True)  # para dbadmin (comprobación de mtd's)
else:
    CONFIG.set_value("StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), False)

CONFIG.set_value("ebcomportamiento/parseProject", False)
# print("temp_dir" + temp_dir)
if temp_dir:
    pineboolib_app.PROJECT.tmpdir = temp_dir

main.startup_framework(SQL_CONN)
pineboolib_app.PROJECT.no_python_cache = False
pineboolib_app.SHOW_CURSOR_EVENTS = False
pineboolib_app.PROJECT.conn_manager.set_max_connections_limit(1000)
