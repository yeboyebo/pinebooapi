ALLOWED_HOSTS = (
    'localhost',
    '127.0.0.1',
    'dbhost'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pruebas',
        'USER': 'juanma',
        'PASSWORD': '55555',
        'HOST': 'dbhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': False
    }
}

StaticLoader = False
