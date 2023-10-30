#!/usr/bin/python3
"""API Entry Point"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
# Create a CORS instance and allow all origins
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Returns a JSON-formatted 404 status code response
    """
    response = jsonify({
        "error": "Not found"
    })
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    port = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port))
