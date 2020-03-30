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

StaticLoader = True
dirs = []
dir_list = os.environ.get('STATIC_LOADER_DIRS')
if dir_list is not None and dir_list != '':
    for pdir in os.environ.get('STATIC_LOADER_DIRS').split(','):
        dirs.append(True)
        dirs.append(pdir)

temp_dir = os.environ.get('TEMPDIR')

