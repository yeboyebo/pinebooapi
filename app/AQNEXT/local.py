import os

allowed = ["localhost", "127.0.0.1", "dbhost", "172.16.251.128"]

if os.environ.get("WEBHOST") is not None:
    allowed_lists = os.environ.get("WEBHOST").split(",")
    for allow in allowed_lists:
        allowed.append(allow)

ALLOWED_HOSTS = tuple(allowed)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DBNAME"),
        "USER": os.environ.get("DBUSER"),
        "PASSWORD": os.environ.get("DBPASSWORD"),
        "HOST": "dbhost",
        "PORT": os.environ.get("DBPORT") or os.environ.get("DBPOST"),
        "ATOMIC_REQUESTS": False,
    }
}

websocket = os.environ.get("WEBSOCKET") or False
dirs_list = []
static_loaders_dirs = os.environ.get("STATIC_LOADER_DIRS") or ""
if static_loaders_dirs:
    for pdir in static_loaders_dirs.split(","):
        dirs_list.append(True)
        dirs_list.append(pdir)


temp_dir = os.environ.get("TEMPDIR") or ""
flfiles = os.environ.get("FLFILES_FOLDER") or ""
dbadmin_enabled = os.environ.get("DBADMIN") or False
clear_python_cache = os.environ.get("CLEAR_PYTHON_CACHE") or False
delete_all_cache = os.environ.get("CLEAR_ALL_CACHE") or False
delete_base_cache = os.environ.get("CLEAR_CACHE_BASE") or False
remove_conn_after_atomic = os.environ.get("REMOVE_CONNECTION_AFTER_ATOMIC") or True
use_alembic_as_altertable = os.environ.get("USE_ALEMBIC") or False
qsa_use_strict_mode = os.environ.get("QSA_USE_STRICK_MODE") or False
enable_acls = os.environ.get("ENABLE_ACLS") or True
show_cursor_events = os.environ.get("SHOW_CURSOR_EVENTS") or False
parse_project_on_init = os.environ.get("PARSE_ALL_PROJECT") or False
use_threads_parser_qsa = os.environ.get("USE_THREADS_ON_QSA_PARSER") or False
allow_alter_table = os.environ.get("ALLOW_ALTER_TABLE") or False

if websocket == "True":
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("dbhost", 6379)],
            },
        },
    }

    # Celery settings
    BROKER_URL = "redis://dbhost:6379/0"  # our redis address
    # use json format for everything
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    ASGI_APPLICATION = "AQNEXT.routing.application"
else:
    WSGI_APPLICATION = "AQNEXT.wsgi.application"
