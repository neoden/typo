from collections import OrderedDict
from typo.core import db


class Post(db.Model):
    __tablename__ = 'posts'

    STATUS = OrderedDict([
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('deleted', 'Удалён')
    ])

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=db.text('now()'), nullable=False)
    author_id = db.Column(db.ForeignKey('users.id', ondelete='restrict'), nullable=False)
    status = db.Column(db.Enum(STATUS.keys(), name='post_status'), server_default='draft', default='draft')
    published = db.Column(db.DateTime(timezone=True), nullable=True)
    title = db.Column(db.String(255))
    markdown = db.Column(db.Text)
    html = db.Column(db.Text)

    author = db.relationship('User', foreign_keys='Post.author_id')
    comments = db.relationship('Comment', order_by='Comment.path')

    @property
    def status_label(self):
        return Post.STATUS[self.status]

    @property
    def allowed_publish(self):
        return self.status == 'draft' or self.id is None

    @property
    def allowed_draft(self):
        return self.status == 'published'

    @property
    def allowed_delete(self):
        return self.status != 'deleted'
