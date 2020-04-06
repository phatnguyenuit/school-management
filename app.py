import logging
import os
from logging.handlers import RotatingFileHandler
from werkzeug.utils import find_modules, import_string

from flask import Flask, jsonify, request, after_this_request

app = Flask(__name__)
app.url_map.strict_slashes = False

for name in find_modules('blueprints'):
    mod = import_string(name)
    if hasattr(mod, 'blueprint'):
        app.register_blueprint(mod.blueprint)

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


@app.route('/')
def index():
    return jsonify(dict(message='Hello World!'))
