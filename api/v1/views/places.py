#!/usr/bin/python3
"""
Create a new view for Place objects that handles all default RESTFul
API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/places/<path:city_id>/places", methods=["GET"],
                 strict_slashes=False)
def all_places(city_id):
    """
    Retrieves the list of all Place objects of a City.
    """
    from models.city import City
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<path:place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object
    """
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<path:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object
    """
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<path:city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place
    """
    from models.city import City
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    data_body = request.get_json(force=True, silent=True)
    if not data_body:
        abort(400, "Not a JSON")

    if 'user_id' not in data_body:
        abort(400, "Missing user_id")

    from models.user import User
    user = storage.get(User, data_body.get("user_id"))

    if user is None:
        abort(404)

    if 'name' not in data_body:
        abort(400, "Missing name")

    from models.place import Place
    place = Place(**data_body)
    place.city_id = city.id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<path:place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object
    """
    from models.place import Place
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data_body = request.get_json(force=True, silent=True)

    if not data_body:
        abort(400, "Not a JSON")

    for key, value in data_body.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
