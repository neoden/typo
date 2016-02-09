from flask.ext.login import LoginManager
from flask.ext.redis import FlaskRedis
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.sendmail import Mail

login_manager = LoginManager()

redis = FlaskRedis()

db = SQLAlchemy()

mail = Mail()