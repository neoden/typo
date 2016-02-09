DEBUG = False

SQLALCHEMY_DATABASE_URI = 'postgresql://typo:typo@localhost:5432/typo'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'change-this!'

ASSET_STORAGE_ROOT = '/var/typo/assets'
ASSET_URL_ROOT = '/assets'

MAIL_MAILER = '/usr/sbin/sendmail'
MAIL_MAILER_FLAGS = '-t'
MAIL_DEBUG = DEBUG
DEFAULT_MAIL_SENDER = 'noreply@typo.ru'
DEFAULT_MAX_EMAILS = None
MAIL_FAIL_SILENTLY = True
MAIL_SUPPRESS_SEND = False

REDIS_URL = 'redis://localhost:6379/0'

MQ_CHANNEL = 'typo'
MQ_POLLING_DELAY = 0.01
