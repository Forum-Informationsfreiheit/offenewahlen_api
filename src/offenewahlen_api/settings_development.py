import os
from offenewahlen_api.settings_user import *
from offenewahlen_api.settings import *


DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
USER_SETTINGS_EXIST = True

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
