import os
from os import path
import sys

PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))
sys.path.insert(0, path.join(PROJECT_ROOT, "../motor/"))
sys.path.insert(1, path.join(PROJECT_ROOT, "apps/"))
sys.path.insert(2, path.join(PROJECT_ROOT, "controllers/"))

from YBAQNEXT.settings import *
from YBAQNEXT.yeboapps import *
from .local import *

# Nivel del logger "django" (con DEBUG registra cada consulta SQL).
LOGGING["loggers"]["django"]["level"] = os.environ.get("DJANGO_LOG_LEVEL", "DEBUG")

# if websocket == "True":
#    INSTALLED_APPS += ('channels', )
