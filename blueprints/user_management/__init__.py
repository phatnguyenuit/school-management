from flask import Blueprint, current_app

from helpers.common import initiate_users

blueprint = Blueprint('users', import_name=__name__, url_prefix='/users')

current_app.logger.info("Blueprint '{}' => Loaded".format(__name__))

INITIAL_USER_SIZE = 100
USERS_DICT = {user['id']: user for user in initiate_users(INITIAL_USER_SIZE)}

# Import all controllers
from . import controllers
from . import models
