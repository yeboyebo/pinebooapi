import os
from .local import *
from pineboolib import application as pineboolib_app
from YBUTILS.DbRouter import get_current_user
from pineboolib.loader.projectconfig import ProjectConfig
from pineboolib.core.settings import CONFIG
from pineboolib.loader import main
from pineboolib.application.parsers import parser_qsa as qsaparser
from pineboolib.core import garbage_collector as gc
from pineboolib import core
import sys
import threading

if external_modules:
    sys.path.insert(0, "/external")

def nombre_session():
    return get_current_user()


def to_bool(texto: str):
    """Convierte en bool."""
    result = str(texto).lower() in ("true", "1")
    return result


pineboolib_app.PROJECT.set_session_function(nombre_session)

SQL_CONN = ProjectConfig(
    database=DATABASES["default"]["NAME"],
    host=DATABASES["default"]["HOST"],
    port=DATABASES["default"]["PORT"],
    type="PostgreSQL (PSYCOPG2)",
    username=DATABASES["default"]["USER"],
    password=DATABASES["default"]["PASSWORD"],
)
if len(dirs_list):
    CONFIG.set_value(
        "StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), True
    )  # Para activar carga estática
    CONFIG.set_value(
        "StaticLoader/%s/dirs" % DATABASES["default"]["NAME"], dirs_list
    )  # Directorios para carga estatica(Configurar en local.py, Ej: dirs = [True, "/home/modulos/api/scripts", True, "/home/modulos/libreria/scripts"])
    CONFIG.set_value("ebcomportamiento/SLConsola", True)  # Muestra debug por consola


else:
    CONFIG.set_value("StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), False)

pineboolib_app.USE_WEBSOCKET_CHANNEL = False

CONFIG.set_value("ebcomportamiento/parseProject", False)

if temp_dir:
    pineboolib_app.PROJECT.tmpdir = temp_dir

qsaparser.USE_THREADS = to_bool(use_threads_parser_qsa)
qsaparser.STRICT_MODE = to_bool(qsa_use_strict_mode)

pineboolib_app.ALLOW_ALTER_TABLE=to_bool(allow_alter_table)
pineboolib_app.PARSE_PROJECT_ON_INIT = to_bool(parse_project_on_init)
pineboolib_app.PROJECT_NAME = project_name
pineboolib_app.EXTERNAL_FOLDER = "/external" if external_modules else None

pineboolib_app.PROJECT.USE_FLFILES_FOLDER = flfiles
pineboolib_app.UPDATE_FLFILES_FROM_FLFOLDER = update_flfiles_from_flfolder
pineboolib_app.PROJECT.db_admin_mode = to_bool(dbadmin_enabled)
pineboolib_app.PROJECT.no_python_cache = to_bool(clear_python_cache)
pineboolib_app.PROJECT.delete_cache = to_bool(delete_all_cache)
pineboolib_app.PROJECT.delete_base_cache = to_bool(delete_base_cache)
pineboolib_app.FRAMEWORK_DEBUG_LEVEL = 30 - (int(debug_level) * 5)
pineboolib_app.PROJECT.conn_manager.set_max_connections_limit(100)

pineboolib_app.USE_ALTER_TABLE_LEGACY = not to_bool(use_alembic_as_altertable)
pineboolib_app.ENABLE_ACLS = to_bool(enable_acls)
pineboolib_app.SHOW_CURSOR_EVENTS = to_bool(show_cursor_events)

main.startup_framework(SQL_CONN)
if not disable_memory_leaks:
    print("Memory leaks check enabled.CANCELED!!")
    
    # core.DISABLE_CHECK_MEMORY_LEAKS = False
    # timer_gc = threading.Timer(interval=0,function=gc.periodic_gc, args=[gb_seconds,])
    # timer_gc.start()

pineboolib_app.PROJECT.conn_manager.REMOVE_CONNECTIONS_AFTER_ATOMIC = to_bool(
    remove_conn_after_atomic
)



pineboolib_app.PROJECT.call("formQUEUE_EVENTS.servicioTareasPendientesInit", [], show_exceptions=False) 
pineboolib_app.PROJECT.call("formCRON.init_cron", [], None, False)



