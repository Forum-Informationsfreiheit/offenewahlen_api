import os
from offenewahlen_api.settings_user import *
from offenewahlen_api.settings import *


DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
USER_SETTINGS_EXIST = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'app.sqlite3')
        }
}
