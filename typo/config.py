DEBUG = False

SQLALCHEMY_DATABASE_URI = 'postgresql://typo:typo@localhost:5432/typo'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'change-this!'

ASSET_STORAGE_ROOT = '/var/typo/assets'
ASSET_URL_ROOT = '/assets'

MAIL_ENABLED = True
MAIL_DEFAULT_SENDER = 'noreply@stoneinfocus.org'
MAIL_SERVER = '127.0.0.1'
MAIL_PORT = 25

REDIS_URL = 'redis://localhost:6379/0'

MQ_CHANNEL = 'typo'
MQ_POLLING_DELAY = 0.01

WTF_CSRF_CHECK_DEFAULT = False
WTF_CSRF_ENABLED = False