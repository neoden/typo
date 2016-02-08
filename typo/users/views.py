from flask import render_template

from . import mod


@mod.route('/login')
def login():
    return render_template('users/login.html')


@mod.route('/logout')
def logout():
    pass


@mod.route('/register')
def register():
    pass