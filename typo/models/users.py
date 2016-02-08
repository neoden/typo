import hashlib

from flask import current_app

from typo.core import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=db.text('now()'), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))

    def __repr__(self):
        return '<User %d:%s>' % (0 if self.id is None else self.id, self.name)

    @staticmethod
    def hash_password(data):
        return hashlib.md5((data + current_app.config['SECRET_KEY']).encode()).hexdigest()

    @property
    def is_active(self):
        return bool(self.roles & 1)

    @property
    def is_authenticated(self):
        return bool(self.roles & 1)

    @property
    def is_anonymous(self):
        return not self.is_authenticated

    def get_id(self):
        return str(self.id)
