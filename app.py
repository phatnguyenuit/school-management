import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, after_this_request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config as DefaultConfig

Config = os.getenv('APP_CONFIG', DefaultConfig)

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    # Register Blueprints
    from blueprints.user_management import blueprint as user_blueprint

    app.register_blueprint(user_blueprint)

# Settings
app.url_map.strict_slashes = False
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/server-log.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%('
            'lineno)d] '
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('- School Management startup -')


@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())
    app.logger.info('Params: %s', request.args)

    @after_this_request
    def log_request_response(response):
        app.logger.info('Status: %s', response.status)
        app.logger.info('Data: %s', response.get_data())
        return response


# Index route
@app.route('/')
def index():
    return jsonify(dict(message='Hello World!'))
