"""
Endpoints for resource data.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.resource import Resource
from models.library import BASEDIR
import os

ALLOWED_EXT = ['png', 'jpeg', 'gif', 'pdf']


def allowed_files(filename):
    """
    Checked if file is allowed for upload
    """

    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXT


@app_views.route('resources', methods=['POST'])
def create_resources():
    """
    Endpoint to create resource
    """

    data = request.get_json()

    if not data:
        return jsonify({'error': 'not a json'})

    if 'title' not in data:
        return jsonify({'error': 'title missing'}), 400
    elif 'type' not in data:
        return jsonify({'error': 'type missing'}), 400
    elif 'content' not in data:
        return jsonify({'error': 'content missing'}), 400

    resource = Resource(**data)
    resource.save()
    return jsonify(resource.to_dict()), 201

@app_views.route('resources/<resource_id>', methods=['GET']
                 , strict_slashes=False)
def get_resource(resource_id):
    """
    route a particular resource data
    """

    resource = storage.get(Resource, resource_id)

    if resource:
        data = resource.to_dict()
        data['userId'] = resource.rack.library.user_id
        return jsonify(data), 200
    return jsonify({'error': 'resource not found'})


@app_views.route('resources/<resource_id>', methods=['PUT']
                , strict_slashes=False)
def update_resource(resource_id):
    """
    updates a resource data
    """

    resource = storage.get(Resource, resource_id)
    data = request.get_json()

    if not resource:
        abort(404)
    if not data:
        return jsonify({"error": "update data missing"})

    resource.update(**data)

@app_views.route('resources/<resource_id>', methods=['DELETE']
                 , strict_slashes=False)
def delete_resource(resource_id):
    """
    deletes a resource
    """

    resource = storage.get(Resource, resource_id)

    if not resource:
        abort(404)

    resource.delete()
    return {'status': 'done'}, 200

@app_views.route('resource/upload', methods=['POST'])
def save_resource_file():
    """
    save user's resource file
    """

    data = request.get_json()
    typ = data.get('type')

    if not typ:
        return jsonify({"error": "type missing"}), 400
    elif typ.capitalize not in storage.classes:
        return jsonify({'error': "unsupported resource type"})

    file = request.files['file']

    # saves uploaded file
    if file and allowed_files(file.filename):
        file_path = os.path.join(BASEDIR, typ + 's', file.filename)
        data['content'] = file_path
        try:
            file.save(file_path)
        except Exception:
            return jsonify({"error": "upload failed"}), 200
        resource = storage.classes[typ](**data)
    return jsonify({"message": "upload successful"}), 200

@app_views.route('resources', strict_slashes=False, methods=['GET'])
def get_resources():
    """
    Routes public resources.
    """
    public_only = request.args.get('public')
    resources = [resource.to_dict() for resource in storage.all(Resource).values()]

    if public_only:
        resources = [resource for resource in resources if resource['public']]

    for resource in resources:
        resource['userId'] = resource.rack.library.user_id

    return jsonify(resources)

