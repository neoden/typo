from flask.ext.login import LoginManager
from flask.ext.redis import FlaskRedis
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

from typo.mail import Mail

login_manager = LoginManager()

redis = FlaskRedis()

db = SQLAlchemy()

mail = Mail()

csrf = CsrfProtect()