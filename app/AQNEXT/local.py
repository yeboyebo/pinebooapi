import os

allowed = ["localhost", "127.0.0.1", "dbhost"]

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
        "HOST": os.environ.get("DBHOST"),
        "PORT": os.environ.get("DBPORT") or os.environ.get("DBPOST"),
        "ATOMIC_REQUESTS": False,
    }
}

dirs_list = []
static_loaders_dirs = os.environ.get("STATIC_LOADER_DIRS") or ""
if static_loaders_dirs:
    for pdir in static_loaders_dirs.split(","):
        dirs_list.append(True)
        dirs_list.append(pdir)


external_modules = os.environ.get("EXTERNAL_MODULES") or False

if external_modules:
    dirs_list.append(True)
    dirs_list.append("/external")


temp_dir = os.environ.get("TEMPDIR") or ""
flfiles = os.environ.get("FLFILES_FOLDER") or ""
update_flfiles_from_flfolder = os.environ.get("UPDATE_FLFILES_FROM_FLFOLDER") or False and flfiles
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
project_name = os.environ.get("PROJECT_NAME") or None
debug_level = os.environ.get("DEBUG_LEVEL") or 2


WSGI_APPLICATION = "AQNEXT.wsgi.application"
