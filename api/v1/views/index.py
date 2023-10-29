#!/usr/bin/python3
"""Module contains routes status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """
    Returns a JSON status.
    """
    return jsonify({"status": "OK"})
