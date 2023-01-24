import os


DB_SCHEME = os.environ.get('DB_SCHEME')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'OPTIONS': {
            # указываем схемы, с которыми будет работать приложение
            'options': f"-c search_path=public,{DB_SCHEME}"
        }
    }
}