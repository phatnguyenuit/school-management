import random
import string
import uuid


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
    for _ in range(1, size + 1):
        random_name = get_random_string(5).capitalize()
        random_email = '{}@example.com'.format(get_random_string(10))

        random_user = dict(
            id=str(uuid.uuid1()),
            name=random_name,
            email=random_email
        )
        yield random_user
