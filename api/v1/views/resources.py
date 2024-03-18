"""
Endpoints for resource data.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.resource import Resource


@app_views.route('resources', methods=['GET', 'POST'])
def resources():
    """
    Endpoint to all resources data
    """


    if request.method == 'GET':
        resources = [resource.to_dict() for resource in\
                     storage.all(Resource).values()]
        return jsonify(resources), 200
    elif request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'not a json'})

        if 'title' not in data:
            return jsonify({'error': 'title missing'}), 400
        elif 'type' not in data:
            return jsonify({'error': 'type missing'}), 400
        elif 'content' not in data:
            return jsonify({'error': 'content missing'}), 400

        resource = storage.classes[data['type']](**data)
        resource.save()

        return jsonify(resource.to_dict()), 201

@app_views.route('resources/<resource_id>')
def resource(resource_id):
    """
    route a particular resource data
    """

    resource = storage.get(Resource, resource_id)

    if resource:
        return jsonify(resource.to_dict())
    return jsonify({'error': 'resource not found'})
