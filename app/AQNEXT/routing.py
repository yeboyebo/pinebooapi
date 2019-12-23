# from channels.routing import route
# from YBUTILS.wsConsumers import *


from channels.routing import ProtocolTypeRouter
from django.urls import path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from YBUTILS.wsConsumers import MyConsumer

application = ProtocolTypeRouter({
    # Channels will do this for you automatically. It's included here as an example.
    # "http": AsgiHandler,

    # Route all WebSocket requests to our custom chat handler.
    # We actually don't need the URLRouter here, but we've put it in for
    # illustration. Also note the inclusion of the AuthMiddlewareStack to
    # add users and sessions - see http://channels.readthedocs.io/en/latest/topics/authentication.html
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path("algo/", MyConsumer),
        ]),
    ),
})

print("________________________________________________")

# from .local import *
# from pineboolib.loader.projectconfig import ProjectConfig
# from pineboolib.core.settings import config
# from pineboolib.loader import main
# from pineboolib.application.parsers import qsaparser

# qsaparser.USE_THREADS = False


# SQL_CONN = ProjectConfig(database=DATABASES["default"]["NAME"], host=DATABASES["default"]["HOST"], port=DATABASES["default"]["PORT"], type="PostgreSQL (PSYCOPG2)", username=DATABASES["default"]["USER"], password=DATABASES["default"]["PASSWORD"])
# if StaticLoader:
#     config.set_value("StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), True)  # Para activar carga estática
#     config.set_value("StaticLoader/%s/dirs" % DATABASES["default"]["NAME"], dirs) # Directorios para carga estatica(Configurar en local.py, Ej: dirs = [True, "/home/modulos/api/scripts", True, "/home/modulos/libreria/scripts"])
#     config.set_value("ebcomportamiento/SLConsola", True)  # Muestra debug por consola
#     config.set_value("application/dbadmin_enabled", True) # para dbadmin (comprobación de mtd's)
# else:
#     config.set_value("StaticLoader/%s/enabled" % (DATABASES["default"]["NAME"]), False)

# main.startup_framework(SQL_CONN)