import os
import json
from flask import Flask
from redis import StrictRedis

from typo.core import login_manager, redis, db
from typo import models


def create_app(cfg=None, purpose=None):
    app = Flask(__name__)

    load_config(app, cfg)

    redis.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    from .users import mod as mod_user
    app.register_blueprint(mod_user)

    from .home import mod as mod_home
    app.register_blueprint(mod_home)

    return app


def load_config(app, cfg=None):
    app.config.from_pyfile('config.py')

    if cfg is not None:
        app.config.from_pyfile(cfg)