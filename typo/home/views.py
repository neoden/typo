import bleach
import markdown

from flask import render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user
from sqlalchemy import desc

from . import mod
from .forms import CommentForm

from typo.core import db
from typo.models import Post, Comment


COMMENT_WHITELIST = (
    'p', 'blockquote', 'ul', 'ol', 'li',
    'em', 'strong', 'a', 'img', 'code', 'pre'
)


@mod.route('/')
def index():
    posts = Post.query.filter_by(status='published').order_by(desc(Post.created)).paginate()
    return render_template('index.html', posts=posts)


@mod.route('/posts/<int:post_id>')
def post(post_id):
    post = Post.query.options(db.joinedload('comments')).get_or_404(post_id)
    return render_template('post.html', post=post)


@mod.route('/posts/<int:post_id>/comment', methods=('POST',))
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)

    form = CommentForm(request.form)

    if form.validate_on_submit():
        comment = Comment(post_id=post.id, author_id=current_user.id, markdown=form.markdown.data)
        dirty_html = markdown.markdown(form.markdown.data, output_format='html5')
        comment.html = bleach.clean(dirty_html, tags=COMMENT_WHITELIST)

        db.session.add(comment)
        db.session.flush()

        if form.replyto.data:
            parent = Comment.query.get_or_404(form.replyto.data)
            comment.path = parent.path
            comment.path.append(comment.id)
        else:
            comment.path = [comment.id]
        db.session.commit()

    return redirect(url_for('home.post', post_id=post.id))
