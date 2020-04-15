from flask import Blueprint, current_app

blueprint = Blueprint('users', import_name=__name__, url_prefix='/users')

current_app.logger.info("Blueprint '{}' => Loaded".format(__name__))

# Import all controllers
from . import controllers
from . import models
