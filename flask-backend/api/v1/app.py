#!/usr/bin/python3
"""
Flask app for REST API
"""

from flask import Flask, jsonify, request
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import  (JWTManager, create_access_token)
import datetime
from models.user import User


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
app.config['JWT_SECRET_KEY'] = 'buswub882e2'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
migrate = Migrate(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
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


@app.route("/api/v1/auth/me", strict_slashes=False, methods=['POST'])
def authenticate():
    # guarded import

    """Authenticate user credentials"""

    credentials = request.get_json()

    if credentials or all(('username', 'password')) in credentials.keys():
        user = storage.find(User, credentials['username']).first()

        if user:
            pwd_hash = user.password
            pwd = credentials['password']

            if bcrypt.check_password_hash(pwd_hash, pwd):
                data = user.to_dict()
                access_token = create_access_token(identity=user.id)
                data['access_token'] = access_token
                return data, 200

    return {"msg": "username or password is incorrect"}, 400


if __name__ == '__main__':
    host = getenv('USOURCE_HOST')
    port = int(getenv('USOURCE_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)

