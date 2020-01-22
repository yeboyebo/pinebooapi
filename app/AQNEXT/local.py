import os

ALLOWED_HOSTS = (
    'localhost',
    '127.0.0.1',
    'dbhost'
)

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

StaticLoader = True
dirs = [True, "/pineboo/modules/fun/ruta/scripts",]