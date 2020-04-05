import logging
import os
import random
import re
import string
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, after_this_request

app = Flask(__name__)

# if app.debug:
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


def paginate(arr):
    def wrap(page=0, page_size=5):
        skip = page * page_size
        to = skip + page_size
        return arr[skip:to]

    return wrap


LETTERS = string.ascii_lowercase


def get_random_string(length=10):
    return ''.join([random.choice(LETTERS) for _ in range(length)])


def initiate_users(size=10):
    for user_no in range(1, size + 1):
        user_id = str(user_no).zfill(4)
        random_name = get_random_string(5).capitalize()
        random_email = '{}@example.com'.format(get_random_string(10))

        random_user = dict(
            id=user_id,
            name=random_name,
            email=random_email
        )
        yield random_user


USERS = [user for user in initiate_users(1000)]


@app.route('/')
def index():
    return jsonify(dict(message='Hello World!'))


@app.route("/users")
def search_users():
    # Filters
    name = request.args.get('name', '')
    email = request.args.get('email', '')

    filtered_users = list(
        filter(
            lambda user: all([
                re.search(email, user.get('email'), re.IGNORECASE),
                re.search(name, user.get('name'), re.IGNORECASE)
            ]),
            USERS
        )
    )

    paginator = paginate(filtered_users)

    # Pagination
    page = request.args.get('page', 0, type=int)
    page_size = request.args.get('pageSize', 5, type=int)
    return jsonify(dict(
        records=paginator(page, page_size),
        page=page,
        pageSize=page_size,
        total=len(filtered_users)
    ))
