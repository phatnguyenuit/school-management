import logging
import os
from logging.handlers import RotatingFileHandler

import click
from flask import request, after_this_request, jsonify, Flask
from flask.cli import AppGroup

from helpers.common import initiate_users
from models import db, migrate


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
    user_cli = AppGroup('users')

    @user_cli.command('init')
    @click.argument('size')
    def create_users(size):
        from blueprints.user_management.models import User
        for index, user_data in enumerate(initiate_users(int(size)), 1):
            user = User(**user_data)
            user.set_password(user_data['email'])

            db.session.add(user)
            db.session.commit()
            app.logger.info(
                '({}/{}) Success! Saved user to DB {}'.format(
                    index, size, user)
            )

    app.cli.add_command(user_cli)
    app.url_map.strict_slashes = False


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
