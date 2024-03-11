"""
Defines endpoints for racks.
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.rack import Rack

@app_views.route('racks', strict_slashes=False, methods=['GET'])
def racks():
    """
    routes public racks.
    """

    racks = [rack.to_dict() for rack in storage.all(Rack).values() if rack.public]

    return jsonify(racks)

@app_views.route('racks/<rack_id>', strict_slashes=False, methods=['GET'])
def rack(rack_id):
    """
    routes to a particular rack data
    """

    rack = storage.get(Rack, rack_id)

    if rack:
        return jsonify(rack.to_dict())
    abort(404)

@app_views.route('racks/<rack_id>/resources/', strict_slashes=False, methods=['GET', 'POST'])
def rack_resources(rack_id):
    """
    routes to a resources of a rack specified with its id.
    """

    if not rack_id:
        abort(404)

    rack = storage.get(Rack, rack_id)

    if rack is None:
        abort(404)

    if request.method == 'GET':
        resources = [resource.to_dict() for resource in rack.resources]

        return jsonify(resources), 200
    elif request.method == 'POST':
        data = request.get_json()

        if 'rack_id' not in data:
            return jsonify({'error': 'missing rack_id'}), 400
        elif 'type' not in data:
            return jsonify({'error': 'missing type'}), 400

        resource = Resource(**data)
        resource.save()


@app_views.route('racks/<rack_id>/subracks',
                 strict_slashes=False, methods=['GET'])
def rack_subracks(rack_id):
    """
    route for subracks of a rack.
    """

    if not rack_id:
        abort(404)

    rack = storage.get(Rack, rack_id)

    if not rack:
        abort(404)

    subracks = [subrack.to_dict() for subrack in rack.subracks]

    return jsonify(subracks), 200
