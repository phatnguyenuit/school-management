import re
import uuid

from flask import jsonify, request

from helpers.common import paginate
from . import blueprint, USERS_DICT


@blueprint.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if any([key not in data for key in ('name', 'email')]):
        return jsonify(message='Missing params'), 400

    user = {**data, 'id': str(uuid.uuid1())}
    USERS_DICT[user['id']] = user
    return jsonify({})


@blueprint.route("/")
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
            USERS_DICT.values()
        )
    )

    paginator = paginate(filtered_users)

    # Pagination
    page = request.args.get('page', 0, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    if page_size > 100:
        return jsonify(
            message='Page size should be less than or equal to 100.'
        ), 400
    return jsonify(dict(
        records=paginator(page, page_size),
        page=page,
        pageSize=page_size,
        total=len(filtered_users)
    ))


@blueprint.route("/<string:user_id>", methods=('GET',))
def get_user(user_id):
    try:
        user = USERS_DICT.get(user_id, None)
        if not user:
            return jsonify(message='User not found'), 404
        return jsonify(user)
    except ValueError:
        return jsonify(message='Wrong user_id'), 404


@blueprint.route("/<string:user_id>", methods=('PUT',))
def update_user(user_id):
    try:
        user = USERS_DICT.get(int(user_id), None)
        if not user:
            return jsonify(message='User not found'), 404
        data = request.get_json()
        USERS_DICT[user['id']] = {**user, **data}
        return jsonify({})
    except ValueError:
        return jsonify(message='Wrong user_id'), 404


@blueprint.route("/<string:user_id>", methods=('DELETE',))
def delete_user(user_id):
    try:
        user = USERS_DICT.get(int(user_id), None)
        if not user:
            return jsonify(message='User not found'), 404
        USERS_DICT.pop(user['id'])
        return jsonify({})
    except ValueError:
        return jsonify(message='Wrong user_id'), 404
