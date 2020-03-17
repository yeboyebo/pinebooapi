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
dirs = []
if os.environ.get('STATIC_LOADER_DIRS') != '':
    for pdir in os.environ.get('STATIC_LOADER_DIRS').split(','):
        dirs.append(True)
        dirs.append(pdir)

temp_dir = os.environ.get('TEMPDIR')

