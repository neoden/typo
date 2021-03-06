import hashlib

from flask import current_app
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from typo.core import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    ROLE_LOGIN = 1
    ROLE_MODERATOR = 2
    ROLE_ADMIN = 2^32 - 1

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=db.text('now()'), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))
    roles = db.Column(db.Integer(), server_default='0', default=0, nullable=False)

    def __repr__(self):
        return '<User %d:%s>' % (0 if self.id is None else self.id, self.name)

    @property
    def is_active(self):
        return bool(self.roles & self.ROLE_LOGIN)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return not self.is_authenticated

    def get_id(self):
        return str(self.id)

    def has_role(self, role):
        return self.roles & role > 0

    def validate_login(self, password):
        return check_password_hash(self.password_hash, password)
