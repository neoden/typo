from flask import Blueprint
from flask.ext.login import current_user, login_required

mod = Blueprint('users', __name__)

from . import views


from typo.models import User
from typo.core import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
