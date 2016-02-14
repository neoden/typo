from flask import render_template, request, redirect

from . import mod

from typo.models import Post


@mod.route('/')
def index():
    posts = Post.query.filter_by(status='published').paginate()
    return render_template('index.html', posts=posts)

