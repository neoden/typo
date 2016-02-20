from flask import render_template, request, redirect, url_for
from flask.ext.login import login_required, current_user

from . import mod

from typo.models import Post
from typo.core import db
from .forms import PostForm, ProfileEditForm


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

    if form.validate_on_submit():
        form.populate_obj(post)
        post.author_id = current_user.get_id()
        if form.publish.data == True:
            post.status = 'published'
        db.session.commit()
        return redirect(url_for('home.index'))

    return render_template('my/post.html', form=form, post=post)


@mod.route('/profile/', methods=('GET', 'POST'))
@login_required
def profile():
    user = current_user
    form = ProfileEditForm(request.form, user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()

    return render_template('my/profile.html', user=user)