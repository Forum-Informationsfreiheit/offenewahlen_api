import os
from offenewahlen_api.settings import *


TESTING = True
SQLALCHEMY_ECHO = True

if 'TRAVIS' in os.environ:
    travis = os.getenv('TRAVIS', default=False)

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'travisci',
			'USER': 'postgres',
			'PASSWORD': '',
			'HOST': 'localhost',
			'PORT': '',
	}
}
elif os.environ['DATABASE_URL']:
    from offenewahlen_api.settings_user import *
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
else:
    from offenewahlen_api.settings_user import *
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
