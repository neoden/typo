from flask import Blueprint
from flask.ext.login import current_user, login_required

mod = Blueprint('home', __name__)

from . import views