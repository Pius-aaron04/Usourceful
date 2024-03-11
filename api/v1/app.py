#!/usr/bin/python3
"""
Flask app for REST API
"""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.errorhandler(404)
def handle_404(error):
    """
    404 error status.
    """

    return jsonify({"error": "not found"}), 404


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Teardown.
    """

    storage.close()


if __name__ == '__main__':
    host = getenv('USOURCE_HOST')
    port = int(getenv('USOURCE_PORT', 5000))
    app.run(host=host, port=port, threaded=True)

