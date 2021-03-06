import bleach
import markdown

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_required, current_user
from sqlalchemy import desc

from . import mod

from typo.models import Post
from typo.core import db
from .forms import PostForm, ProfileEditForm
from typo.util import flash_errors


POST_WHITELIST = (
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote',
    'ul', 'ol', 'li', 'em', 'strong', 'a', 'img', 'code', 'pre'
)


@mod.route('/posts/new/', methods=('GET', 'POST'))
@mod.route('/posts/<int:post_id>/edit/', methods=('GET', 'POST'))
@login_required
def post(post_id=None):
    if post_id:
        post = Post.query.get_or_404(post_id)
    else:
        post = Post()
        db.session.add(post)

    form = PostForm(request.form, post)

    if request.method == 'POST':
        if form.status.data == 'deleted':
            post.status = 'deleted'
            db.session.commit()
            flash('Пост удалён', 'info')
            return redirect(url_for('home.index'))
        elif form.validate_on_submit():
            form.populate_obj(post)
            post.author_id = current_user.get_id()
            dirty_html = markdown.markdown(form.markdown.data, output_format='html5')
            post.html = bleach.clean(dirty_html, tags=POST_WHITELIST)
            db.session.commit()
            return redirect(url_for('home.index'))
        else:
            flash_errors(form)

    return render_template('my/post.html', form=form, post=post)


@mod.route('/posts/')
@login_required
def posts():
    posts = Post.query.filter(Post.author_id == current_user.get_id(), Post.status != 'deleted')\
                      .order_by(desc(Post.created))
    pagination = posts.paginate()
    return render_template('my/posts.html', posts=pagination)


@mod.route('/profile/', methods=('GET', 'POST'))
@login_required
def profile():
    user = current_user
    form = ProfileEditForm(request.form, user)

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
        else:
            flash_errors(form)

    return render_template('my/profile.html', user=user)