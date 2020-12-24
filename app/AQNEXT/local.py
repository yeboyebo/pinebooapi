import os

allowed = ['localhost', '127.0.0.1', 'dbhost']

if os.environ.get('WEBHOST') is not None:
    allowed.append(os.environ.get('WEBHOST'))

ALLOWED_HOSTS = tuple(allowed)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DBNAME'),
        'USER': os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASSWORD'),
        'HOST': 'dbhost',
        'PORT': os.environ.get('DBPOST'),
        'ATOMIC_REQUESTS': False
    }
}

websocket = os.environ.get('WEBSOCKET') or False
USE_ATOMIC_LIST = os.environ.get('USE_ATOMIC_LIST') or False
StaticLoader = True
dirs = []
dir_list = os.environ.get('STATIC_LOADER_DIRS')
if dir_list is not None and dir_list != '':
    for pdir in os.environ.get('STATIC_LOADER_DIRS').split(','):
        dirs.append(True)
        dirs.append(pdir)

temp_dir = os.environ.get('TEMPDIR')

if websocket == "True":
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                'hosts': [('dbhost', 6379)],
            },
        },
    }

    # Celery settings dbhost
    BROKER_URL = 'redis://dbhost:6379/0'  # our redis address
    # use json format for everything
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    ASGI_APPLICATION = "AQNEXT.routing.application"
else:
    WSGI_APPLICATION = 'AQNEXT.wsgi.application'
