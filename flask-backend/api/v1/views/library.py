"""
Endpoints for Libraries
"""

from flask import Flask, jsonify
from models import storage
from models.library import Library
from api.v1.views import app_views

@app_views.route('libraries', methods=['GET'], strict_slashes=False)
def public_libraries():
    """
    Render data of Libraries with public set to true.
    """

    pub_libraries = [lib.to_dict() for lib in storage.all(Library).values() if lib.public]

    return jsonifiy(pub_libraries)

@app_views.route('libraries/<library_id>',
                 methods=['GET'], strict_slashes=False)
def library(library_id):
    """
    Route data for specific library
    """

    if not library_id:
        abort(404)

    lib = storage.get(Library, library_id)

    if lib:
        return jsonify(lib.to_dict()), 200
    abort(404)


@app_views.route('libraries/<library_id>/racks', strict_slashes=False,
                 methods=['GET'])
def library_racks(library_id):
    """
    gets a library racks
    """

    lib = storage.get(Library, library_id)
    if not lib:
        abort(404)
    racks = [rack.to_dict() for rack in library.rack]

    return jsonify(racks), 200
