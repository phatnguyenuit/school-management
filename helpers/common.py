import random
import string
import uuid

import requests
from flask import current_app


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
    results = get_random_users(size)
    current_app.logger.info('Got {} random users'.format(size))
    for user_data in results:
        random_user = dict(
            id=str(uuid.uuid1()),
            name="{} {}".format(
                user_data['name']['first'],
                user_data['name']['last']
            ),
            email=user_data['email']
        )
        yield random_user


def get_random_users(size=10):
    # API to get random user "https://randomuser.me/api"
    params = {
        'results': size,
        'nat': 'us',
    }
    response = requests.get("https://randomuser.me/api", params=params)

    if not response or not response.ok:
        return []

    data = response.json()

    results = data['results']

    return results
