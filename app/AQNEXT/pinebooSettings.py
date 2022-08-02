import os
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
CONFIG.set_value("application/callFunction", "formCRON.init_cron")

if temp_dir:
    pineboolib_app.PROJECT.tmpdir = temp_dir

pineboolib_app.PROJECT.conn_manager.REMOVE_CONNECTIONS_AFTER_ATOMIC = True
# pineboolib_app.PROJECT.conn_manager.SAFE_TIME_SLEEP = 0.1
# pineboolib_app.PROJECT.conn_manager.set_safe_mode(2)

# pineboolib_app.USE_ALTER_TABLE_LEGACY = False

flfiles = os.environ.get('FLFILES_FOLDER')
if flfiles:
    pineboolib_app.PROJECT.USE_FLFILES_FOLDER=flfiles

pineboolib_app.PROJECT.setDebugLevel(200)

pineboolib_app.PROJECT.conn_manager.set_max_connections_limit(100)
main.startup_framework(SQL_CONN)
pineboolib_app.PROJECT.no_python_cache = False
pineboolib_app.SHOW_CURSOR_EVENTS = False
