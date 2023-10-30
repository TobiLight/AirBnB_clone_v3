#!/usr/bin/python3
"""
Create a new view for the link between Place objects and Amenity that handles
all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def place_all_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place.

    Args:
        place_id (string): Place object ID

    Returns:
        The list of all Amenity objects of a Place.
    """
    from models.place import Place
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<path:place_id>/amenities/<path:amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object.

    Args:
        place_id (string): Place object ID
        amenity_id (string): Amenity object ID

    Returns:
        An empty dictionary with status code 200
    """
    from models.place import Place
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    from models.amenity import Amenity
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place

    Args:
        place_id (string): Place object ID
        amenity_id (string): Amenity object ID

    Returns:
        The Amenity with the status code 201
    """
    from models.place import Place
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    from models.amenity import Amenity
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
