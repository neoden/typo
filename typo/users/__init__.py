from flask import Blueprint
from flask.ext.login import current_user, login_required

mod = Blueprint('users', __name__)

from . import views