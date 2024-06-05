#!/usr/bin/python3
"""
Flask app for REST API
"""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
migrate = Migrate(app)
bcrypt = Bcrypt(app)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

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

