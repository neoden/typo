# coding=utf-8

from fabric.api import run, cd, env, prefix, sudo

env.user = 'xtal'


def prod():
    env.env = 'prod'
    env.hosts = ['stoneinfocus.org']
    env.dir = '/srv/web/typo'
    env.venv = 'typo'
    env.app_service = 'typo.service'


def pull():
    print('Обновляем приложение')
    with(cd(env.dir)):
        run('git pull origin master')


def pip():
    print('Устанавливаем завимости')
    with(cd(env.dir)):
        with(prefix('workon ' + env.venv)):
            run('pip install -r requirements.txt')


def migrate():
    print('Накатываем миграции')
    with(cd(env.dir)):
        with(prefix('workon ' + env.venv)):
            run('alembic upgrade head')


def restart():
    print('Перезапускаем ' + env.app_service)
    sudo('systemctl restart ' + env.app_service)


def deploy():
    pull()
    pip()
    migrate()
    restart()
