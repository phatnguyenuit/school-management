import logging
import os
from logging.handlers import RotatingFileHandler

from flask import request, after_this_request, jsonify, Flask
from flask_migrate import Migrate

from models import db

migrate = Migrate()


# Register Blueprints
def register_blueprints(app):
    with app.app_context():
        from blueprints.user_management import blueprint as user_blueprint
        app.register_blueprint(user_blueprint)


def init_database(app):
    db.init_app(app)
    migrate.init_app(app, db)


# Settings
def setting_app(app):
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


def config_logging(app):
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


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or {})
    init_database(app)
    register_blueprints(app)

    setting_app(app)
    config_logging(app)

    @app.route('/')
    def index():
        return jsonify(message='Hi there!')

    return app
