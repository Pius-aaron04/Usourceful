#!/usr/bin/python3

"""
Endpoints for users data
"""

from models import storage
from models.rack import Rack
from models.resource import Resource
from models.user import User
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.library import Library
from .utility import check_attributes
from flask_jwt_extended import jwt_required, get_jwt_identity


@app_views.route("users", methods=['GET'])
def all_users():
    """Gets users"""

    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users), 200

@app_views.route("users/<user_id>", methods=['GET'])
@jwt_required()
def get_user(user_id=None):
    """
    routes user(s) data.
    """

    user = storage.get(User, user_id)

    if not user:
        return jsonify({'error': 'user not found'}), 404

    return jsonify(user.to_dict()), 200


@app_views.route('users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    enpoint to delete user
    """

    user = storage.get(User, user_id)

    if user:
        data = user.to_dict()
        user.delete()
        return jsonify(data), 200
    abort(404)


@app_views.route('users/<user_id>/library/racks', methods=['GET', 'POST'],
                 strict_slashes=False)
@jwt_required()
def user_racks(user_id):
    """
    routes user library racks
    """

    if not user_id:
        abort(404)
    jwt_get_user = get_jwt_identity()
    user = storage.get(User, jwt_get_user)

    if not user:
        return jsonify({'error': 'user not found'}), 404

    if request.method == 'GET':
        user_racks = [rack.to_dict() for rack in user.library.racks]
        return jsonify(user_racks)

    # creates a new rack on POST request
    data = request.get_json()
    print(data)
    check = check_attributes('Rack', set(data)) # checks for required attrs
    if check != 'OK':
        return jsonify(check), 400
    rack = Rack(**data)
    rack.save()
    return jsonify(rack.to_dict()), 201


@app_views.route('users/<user_id>/library/racks/<rack_id>',
                 methods=['PUT', 'DELETE'], strict_slashes=False)
@jwt_required()
def update_delete_user_rack(user_id, rack_id):
    """
    Endpoint to update user's rack
    """

    user = storage.get(User, user_id)
    rack = storage.get(Rack, rack_id)

    if all(user, rack):
        abort(404)

    if request.method == 'PUT':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Update data cannot be empty'})
        rack.update(**data)

        return jsonify(rack.to_dict), 200
    data = rack.to_dict()
    rack.delete()
    return jsonify(data), 200


@app_views.route('users/<user_id>/library/racks/<rack_id>/resources',
                 methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user_rack_resources(user_id, rack_id):
    """
    fetches user's rack resources
    """
    
    user = storage.get(User, user_id)
    rack = storage.get(Rack, rack_id)

    if not (user and rack):
        abort(404)
    
    if request.method == 'GET':
        resources = [res.to_dict() for res in rack.resources]
        return jsonify(resources), 200


@app_views.route('users/<user_id>/library/racks/<rack_id>/resources/',
                 methods=['POST'], strict_slashes=False)
@jwt_required()
def create_rack_resource(user_id, rack_id):
    """
    gets or delete a resource
    """

    user = storage.get(User, user_id)
    rack = storage.get(Rack, rack_id)

    if not (all((user, rack)) and (rack in user.library.racks)):
        abort(404)
    data = request.get_json()
    check = check_attributes('Resource', set(data))

    if check != 'OK':
        return jsonify(check), 400

    resource = Resource(**data)
    resource.save()

    return jsonify(resource.to_dict()), 201


@app_views.route('users/<user_id>/library/racks/<rack_id>/resources/'+\
                 '<resource_id>', methods=['GET', 'PUT'], strict_slashes=False)
@jwt_required()
def get_del_rack_resource(user_id, rack_id, resource_id):
    """
    gets or delete a resource
    """

    user = storage.get(User, user_id)
    rack = storage.get(Rack, rack_id)

    resource = storage.get(Resource, resource_id)

    if not (all((user, resource, rack)) and \
            (rack in user.library.racks and resource in rack.resources)):
        abort(404)

    if request.method == 'PUT':
        if resource.rack.library.user_id != user_id:
            return {"error": "Unauthorized operation"}, 400
        data = request.get_json()
        if not data:
            return {"error": "Unsupported operation(update data missing)"}
        resource.update(**data)
        resource.save()
        return jsonify(resource.to_dict()), 200

    data['userId'] = resource.rack.library.user_id

    return jsonify(data), 200


@app_views.route('users/<user_id>/recommendations', methods=['GET'],
                 strict_slashes=False)
def user_recommendations(user_id):
    """
    Routes recommendations related to user(made by user)
    """

    user = storage.get(User, user_id)

    if not user:
        return jsonify({'error': 'user not found'}), 404

    recommends = [recomm.to_dict() for recomm in user.recommendations]

    return jsonify(recommends), 200


@app_views.route('users', methods=['POST'],
                 strict_slashes=False)
@jwt_required()
def create_user():
    """
    endpoint to create a new user
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "Empty data for creation"}), 400

    if 'firstname' not in data:
        return jsonify({"error": "firstname missing"}), 400
    elif 'lastname' not in data:
        return jsonify({'error': 'lastname missing'}), 400
    elif 'username' not in data:
        return jsonify({'error': 'username missing'}), 400
    elif 'password' not in data:
        return jsonify({'error': 'password missing'}), 400

    # checks for already existing user account
    if storage.find(User, data['username']).first() or\
        storage.find(User, data["email"]).first():
        return {"error": "user already exists"}, 400

    user = User(**data)
    user.save()
    library = Library(**{'name': '{}'.format(user.username), 'user_id': user.id})
    library.save()

    return jsonify(user.to_dict()), 200
