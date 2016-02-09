import uuid

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, logout_user
from werkzeug.security import generate_password_hash

from typo.models import User
from typo.core import db, redis, mail

from . import mod
from .forms import LoginForm, RegisterForm


@mod.route('/login', methods=['POST'])
def login():  
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()

        if User.roles & User.ROLE_LOGIN == 0:
            flash('Пользователь заблокирован', 'error')
        elif user and User.validate_login(user.password_hash, form.password.data):
            login_user(user)
            #flash("Добро пожаловать", category='success')
            return redirect(request.args.get("next") or url_for('.index'))
        else:
            flash("Неверный логин или пароль", category='error')

    return redirect(url_for('home.index'))


@mod.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.password.data != form.password2.data:
                flash("Пароли не совпадают", category='error')
            else:
                user = User.query.filter_by(email=form.email.data).first()
                if user:
                    flash("Пользователь с таким email уже зарегистрирован", category="warning")
                else:
                    user = User(
                        email=form.email.data,
                        password_hash=generate_password_hash(form.password.data),
                        name=form.nickname.data
                    )
                    db.session.add(user)
                    db.session.commit()

                    token = 'register:{}'.format(uuid.uuid4().hex)
                    redis.set(token, user.id, 60 * 60 * 24)

                    mail.send_message(
                        subject='Подтверждение регистрации',
                        recipients=[user.email],
                        html=render_template('email/activate.html', token=token, user_id=user.id),
                        body=render_template('email/activate.txt', token=token, user_id=user.id)
                    )

                    flash('Письмо с запросом на подтверждение регистрации выслано на адрес {}'.format(user.email), 'info')

                    return redirect(url_for('home.index'))

    return render_template('users/register.html', form=form)


@mod.route('/activate')
def activate():
    token = request.get('token', '')
    user_id = request.get('user_id', 0, int)

    key = 'register:{}'.format(token)

    if redis.get(key) == user_id:
        redis.delete(key)

        user = User.get_or_404(user_id)
        login_user(user)

        flash("Добро пожаловать", category='success')
        return redirect(request.args.get("next") or url_for('.index'))
    else:
        flash('Ссылка для активации устарела', 'error')
        return redirect(url_for('home.index'))
