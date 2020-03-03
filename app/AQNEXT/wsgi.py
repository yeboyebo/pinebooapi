"""
WSGI config for AQNEXT project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AQNEXT.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from .local import *
from YBUTILS.DbRouter import get_current_user
from pineboolib.loader.projectconfig import ProjectConfig
from pineboolib.core.settings import config
from pineboolib.loader import main
from pineboolib.application.parsers import qsaparser
from pineboolib import application as pineboolib_app
qsaparser.USE_THREADS = False


def nombre_session():
    return get_current_user()


pineboolib_app.PROJECT.set_session_function(nombre_session)

SQL_CONN = ProjectConfig(database=DATABASES["default"]["NAME"], host=DATABASES["default"]["HOST"], port=DATABASES["default"]["PORT"], type="PostgreSQL (PSYCOPG2)", username=DATABASES["default"]["USER"], password=DATABASES["default"]["PASSWORD"])
if StaticLoader:
    config.set_value("StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), True)  # Para activar carga estática
    config.set_value("StaticLoader/%s/dirs" % DATABASES["default"]["NAME"], dirs)  # Directorios para carga estatica(Configurar en local.py, Ej: dirs = [True, "/home/modulos/api/scripts", True, "/home/modulos/libreria/scripts"])
    config.set_value("ebcomportamiento/SLConsola", True)   # Muestra debug por consola
    config.set_value("application/dbadmin_enabled", True)  # para dbadmin (comprobación de mtd's)
else:
    config.set_value("StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), False)

main.startup_framework(SQL_CONN)
pineboolib_app.SHOW_CURSOR_EVENTS = False
pineboolib_app.PROJECT.conn_manager.set_max_connections_limit(1000)
