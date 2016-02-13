from flask import render_template

from . import mod

from typo.users.forms import LoginForm


@mod.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)
