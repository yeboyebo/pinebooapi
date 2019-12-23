ALLOWED_HOSTS = (
    'localhost',
    '127.0.0.1',
    'dbhost'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '__dbname__',
        'USER': '__dbuser__',
        'PASSWORD': '__dbpassword__',
        'HOST': 'dbhost',
        'PORT': '__dbport__',
        'ATOMIC_REQUESTS': False
    }
}

StaticLoader = False
