
from flask import jsonify, request

from models import db
from . import blueprint
from .models import User


@blueprint.route('/', methods=['POST'])
def create_user():
    payload = request.get_json()
    if any([key not in payload for key in ('name', 'email')]):
        return jsonify(message='Missing params'), 400
    email = payload.get('email')
    if User.query.filter_by(email=email).first():
        return jsonify(
            message='Email was existed.'
        ), 400
    user = User(**payload)
    db.session.add(user)
    db.session.commit()
    return jsonify({})


@blueprint.route("/")
def search_users():
    # Filters
    name = request.args.get('name', '')
    email = request.args.get('email', '')

    query = User.query.filter(
        User.name.ilike('%{}%'.format(name)),
        User.email.ilike('%{}%'.format(email)),
    )

    # Pagination
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)

    if page_size > 100:
        return jsonify(
            message='Page size should be less than or equal to 100.'
        ), 400

    pagination = query.paginate(page, page_size, error_out=False)
    records = pagination.items or []
    total = pagination.total
    return jsonify(dict(
        records=[record.serialize for record in records],
        page=page,
        pageSize=page_size,
        total=total
    ))


@blueprint.route("/<string:user_id>", methods=('GET',))
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify(message='User not found'), 404
        return jsonify(user.serialize)
    except ValueError:
        return jsonify(message='Wrong user_id'), 404


@blueprint.route("/<string:user_id>", methods=('PUT',))
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify(message='User not found'), 404
        data = request.get_json()
        user.update(**data)
        db.session.commit()
        return jsonify({})
    except ValueError:
        return jsonify(message='Wrong user_id'), 404


@blueprint.route("/<string:user_id>", methods=('DELETE',))
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify(message='User not found'), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({})
    except ValueError:
        return jsonify(message='Wrong user_id'), 404
