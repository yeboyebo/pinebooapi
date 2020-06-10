from os import path
import sys
# WSGI_APPLICATION = 'AQNEXT.wsgi.application'
ASGI_APPLICATION = "AQNEXT.routing.application"
PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))

sys.path.insert(0, path.join(PROJECT_ROOT, "../motor/"))
sys.path.insert(1, path.join(PROJECT_ROOT, "apps/"))
sys.path.insert(2, path.join(PROJECT_ROOT, "controllers/"))

from YBAQNEXT.settings import *
from YBAQNEXT.yeboapps import *
from .local import *
