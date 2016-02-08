DEBUG = False

SQLALCHEMY_DATABASE_URI = 'postgresql://typo:typo@localhost:5432/typo'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'change-this!'

ASSET_STORAGE_ROOT = '/var/typo/assets'
ASSET_URL_ROOT = '/assets'

MAIL_ENABLED = True
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = DEBUG
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = 'noreply@typo.ru'

REDIS_URL = 'redis://localhost:6379/0'

MQ_CHANNEL = 'typo'
MQ_POLLING_DELAY = 0.01
