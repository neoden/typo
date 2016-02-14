from flask import Blueprint
from flask.ext.login import current_user, login_required

mod = Blueprint('my', __name__, url_prefix='/my')

from . import views