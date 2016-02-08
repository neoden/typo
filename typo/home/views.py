from flask import render_template

from . import mod


@mod.route('/')
def index():
    return render_template('index.html')
