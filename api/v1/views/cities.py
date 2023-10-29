#!/usr/bin/python3
"""
Create a new view for City objects that handles all default RESTFul
API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/states/<path:state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def all_cities(state_id):
    """
    Retrieves the list of all City objects of a State.
    """
    from models.state import State
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<path:city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object
    """
    from models.city import City
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<path:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a State object
    """
    from models.city import City
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<path:state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City
    """
    from models.state import State
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    data_body = request.get_json(force=True, silent=True)
    if not data_body:
        abort(400, "Not a JSON")

    if 'name' not in data_body:
        abort(400, "Missing name")

    from models.city import City
    city = City(**data_body)
    city.state_id = state.id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<path:city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object
    """
    from models.city import City
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    data_body = request.get_json(force=True, silent=True)

    if not data_body:
        abort(400, "Not a JSON")

    city.name = data_body.get("name", city.name)
    city.save()
    return jsonify(city.to_dict()), 200
