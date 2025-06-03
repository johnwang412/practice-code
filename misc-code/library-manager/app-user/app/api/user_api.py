from flask import jsonify, request

from app.database import database_conn
from app.data import user_data
from app.models.user_orm import User


def create_user():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    with database_conn.get_db_session() as db_session:
        user_orm: User = user_data.add_user(db_session, first_name, last_name)
        db_session.commit()

        return jsonify({'user_id': user_orm.id}), 200


def get_user():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    with database_conn.get_db_session() as db_session:
        user_orm: User = user_data.get_user_by_id(db_session, user_id)
        if not user_orm:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user_id': user_orm.id,
            'first_name': user_orm.first_name,
            'last_name': user_orm.last_name
        }), 200


def add_routes(flask_app):
    flask_app.add_url_rule('/user', methods=['POST'], view_func=create_user)
    flask_app.add_url_rule('/user', methods=['GET'], view_func=get_user)
