from flask import flash
from flask import current_app as app


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            if app.config['DEBUG']:
                flash('{}: {}'.format(field, error), 'danger')
            else:
                flash(error, 'danger')
