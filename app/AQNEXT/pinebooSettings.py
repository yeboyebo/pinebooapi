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
import os
import threading
from pineboolib.application.database import pnconnectionmanager


def _enumerate_seguro(self):
    """Igual que PNConnectionManager.enumerate pero iterando sobre una copia.

    El original recorre connections_dict mientras otros hilos añaden o quitan conexiones
    ("dictionary changed size during iteration" con varios hilos sirviendo peticiones).
    """
    dict_ = {}
    id_thread = str(threading.current_thread().ident)
    for key, value in list(self.connections_dict.items()):
        connection_data = key.split("|")
        if connection_data[0] == id_thread:
            dict_[connection_data[1]] = value
    return dict_


pnconnectionmanager.PNConnectionManager.enumerate = _enumerate_seguro


def nombre_session():
    return get_current_user()


pineboolib_app.PROJECT.set_session_function(nombre_session)

SQL_CONN = ProjectConfig(database=DATABASES["default"]["NAME"], host=DATABASES["default"]["HOST"], port=DATABASES["default"]["PORT"], type="PostgreSQL (PSYCOPG2)", username=DATABASES["default"]["USER"], password=DATABASES["default"]["PASSWORD"])
if StaticLoader:
    CONFIG.set_value("StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), True)  # Para activar carga estática
    CONFIG.set_value("StaticLoader/%s/dirs" % DATABASES["default"]["NAME"], dirs)  # Directorios para carga estatica(Configurar en local.py, Ej: dirs = [True, "/home/modulos/api/scripts", True, "/home/modulos/libreria/scripts"])
    CONFIG.set_value("ebcomportamiento/SLConsola", True)   # Muestra debug por consola
    CONFIG.set_value("application/dbadmin_enabled", True)  # para dbadmin (comprobación de mtd's)
else:
    CONFIG.set_value("StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), False)

pineboolib_app.SHOW_CLOSED_CONNECTION_WARNING = False
pineboolib_app.USE_ATOMIC_LIST = USE_ATOMIC_LIST
pineboolib_app.USE_WEBSOCKET_CHANNEL = True
CONFIG.set_value("ebcomportamiento/parseProject", False)

if temp_dir:
    pineboolib_app.PROJECT.tmpdir = temp_dir

# Pool de SQLAlchemy por proceso: pool_size=N y max_overflow=N+10. Con 100 (el valor de siempre)
# runserver acumulaba decenas de conexiones inactivas; en producción se fija en el Deployment.
pineboolib_app.PROJECT.conn_manager.set_max_connections_limit(int(os.environ.get("POOL_CONNECTION_LIMIT", 100)))
main.startup_framework(SQL_CONN)
pineboolib_app.PROJECT.no_python_cache = False
pineboolib_app.SHOW_CURSOR_EVENTS = False
