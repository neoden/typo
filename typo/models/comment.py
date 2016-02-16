from sqlalchemy.dialects.postgresql import ARRAY

from typo.core import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=db.text('now()'), nullable=False)
    deleted = db.Column(db.Boolean, server_default='false', default=False, nullable=False)
    post_id = db.Column(db.ForeignKey('posts.id'), nullable=False, index=True)
    author_id = db.Column(db.ForeignKey('users.id'), nullable=False, index=True)
    path = db.Column(ARRAY(db.Integer()), nullable=True)
    text = db.Column(db.Text(), nullable=False)

    post = db.relationship('Post')
    author = db.relationship('User')

    @property
    def level(self):
        return str(len(self.path)) if len(self.path) else '10plus'
    