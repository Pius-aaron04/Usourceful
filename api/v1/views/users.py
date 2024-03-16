#!/usr/bin/python3

"""
Endpoints for users data
"""

from models import storage
from models.user import User
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route("users", methods=['GET'])
@app_views.route("users/<user_id>", methods=['GET'])
def users(user_id=None):
    """
    routes user(s) data.
    """

    if not user_id:
        users = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users), 200

    user = storage.get(User, user_id)

    if not user:
        return jsonify({'error': 'user not found'}), 404

    return jsonify(user.to_dict()), 200

@app_views.route('users/<user_id>/library', methods=['GET'])
def user_library(user_id):
    """
    route user library data
    """

    user = storage.get(User, user_id)

    if not user:
        return jsonify({'error': 'user not found'}), 404

    return jsonify(user.library.to_dict()), 200


@app_views.route('users/<user_id>/library/racks', methods=['GET'])
def user_racks(user_id):
    """
    routes user library racks
    """

    user = storage.get(User, user_id)

    if user:
        user_racks = [rack.to_dict() for rack in user.library.racks]
        return jsonify(user_racks)
    return jsonify({'error': 'user not found'}), 404

@app_views.route('users/<user_id>/recommendations', methods=['GET'])
def user_recommendations(user_id):
    """
    Routes recommendations related to user(made by user)
    """

    user = storage.get(User, user_id)

    if not user:
        return jsonify({'error': 'user not found'}), 404

    recommends = [recomm.to_dict() for recomm in user.recommendations]

    return jsonify(recommends), 200
