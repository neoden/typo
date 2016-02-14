from typo.core import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=db.text('now()'), nullable=False)
    author_id = db.Column(db.ForeignKey('users.id', ondelete='restrict'), nullable=False)
    status = db.Column(db.Enum('draft', 'published', 'deleted', name='post_status'), server_default='draft', default='draft')
    published = db.Column(db.DateTime(timezone=True), nullable=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
