import os
from offenewahlen_api.settings_user import *
from offenewahlen_api.settings import *


DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
USER_SETTINGS_EXIST = True

if os.environ.get('SQLALCHEMY_DATABASE_URI') is None:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'app.sqlite3')
            }
    }
else:
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
