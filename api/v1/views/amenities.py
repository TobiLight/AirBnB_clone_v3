#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles all default RESTFul
API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """
    Retrieves the list of all Amenity objects.
    """
    amenities = [amenity.to_dict()
                 for amenity in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route("/amenities/<path:amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves an Amenity object
    """
    from models.amenity import Amenity
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<path:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object
    """
    from models.amenity import Amenity
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """
    Creates an Amenity
    """
    data_body = request.get_json(force=True, silent=True)
    if not data_body:
        abort(400, "Not a JSON")

    if 'name' not in data_body:
        abort(400, "Missing name")

    from models.amenity import Amenity
    amenity = Amenity(**data_body)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<path:amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a amenity object
    """
    from models.amenity import amenity
    amenity = storage.get(amenity, amenity_id)

    if amenity is None:
        abort(404)

    data_body = request.get_json(force=True, silent=True)

    if not data_body:
        abort(400, "Not a JSON")

    amenity.name = data_body.get("name", amenity.name)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
