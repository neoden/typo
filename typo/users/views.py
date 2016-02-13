import uuid

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, logout_user
from werkzeug.security import generate_password_hash

from typo.models import User
from typo.core import db, redis, mail, csrf

from . import mod
from .forms import LoginForm, RegisterForm


@mod.route('/login', methods=['POST'])
def login():  
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()

        if user:
            if user.validate_login(form.password.data):
                if user.has_role(User.ROLE_LOGIN):
                    login_user(user)
                    #flash("Добро пожаловать", category='success')
                    return redirect(request.args.get("next") or url_for('home.index'))
                else:
                    flash('Пользователь заблокирован', 'error')
            else:
                flash("Неверный логин или пароль", category='error')
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
                    registration_data = {
                        'name': form.nickname.data,
                        'email': form.email.data,
                        'password_hash': generate_password_hash(form.password.data)
                    }

                    token = uuid.uuid4().hex
                    key = 'register:{}'.format(token)
                    redis.hmset(key, registration_data)
                    redis.expire(key, 60 * 60 * 24)

                    mail.send(
                        subject='Подтверждение регистрации',
                        recipients=[form.email.data],
                        html=render_template('email/activate.html', token=token),
                        text=render_template('email/activate.txt', token=token)
                    )

                    flash('Письмо с запросом на подтверждение регистрации выслано на адрес {}'.format(form.email.data), 'info')

                    return redirect(url_for('home.index'))

    return render_template('users/register.html', form=form)


@mod.route('/activate')
def activate():
    token = request.args.get('token', '')

    key = 'register:{}'.format(token)

    registration_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in redis.hgetall(key).items()}
    if registration_data:
        redis.delete(key)

        user = User(roles=User.ROLE_LOGIN, **registration_data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Добро пожаловать", category='success')
        return redirect(request.args.get("next") or url_for('home.index'))
    else:
        flash('Ссылка для активации устарела', 'error')
        return redirect(url_for('home.index'))
