#!/usr/bin/python3
"""
Create a new view for Place objects that handles all default RESTFul
API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route("/cities/<path:city_id>/places", methods=["GET"],
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

    if 'name' not in data_body:
        abort(400, "Missing name")

    from models.user import User
    data_body['city_id'] = city_id
    user = storage.get(User, data_body['user_id'])

    if user is None:
        abort(404)

    from models.place import Place
    place = Place(**data_body)
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """
    data_body = request.get_json(force=True, silent=True)
    if data_body is None:
        abort(400, "Not a JSON")

    states = data_body.get("states", [])
    cities = data_body.get("cities", [])
    amenities = data_body.get("amenities", [])

    if not data_body or len(data_body) < 1 or not states\
            and cities and amenities:
        from models.place import Place
        places_list = storage.all(Place).values()
        places = [place.to_dict() for place in places_list]
        return jsonify(places), 200

    # if states is specified and cities isnt
    if len(states) > 0 and not cities:
        cities_in_states = []
        for sid in states:
            from models.state import State
            state = storage.get(State, sid)
            for city_in_state in state.cities:
                cities_in_states.append(city_in_state)
        places_in_city = []
        for city_in_state in cities_in_states:
            for place in city_in_state.places:
                places_in_city.append(place.to_dict())

        places_in_cities = [place for place in places_in_city]
        return jsonify(places_in_cities), 200

    # if cities is specified and states isnt
    if len(cities) > 0 and not len(states):
        places = []
        places_in_cities = []
        for cid in cities:
            from models.city import City
            city = storage.get(City, cid)
            for place_in_city in city.places:
                places_in_cities.append(place_in_city.to_dict())

        places_in_city = [place for place in places_in_cities]
        return jsonify(places_in_city), 200

    # if states and cities are both specified
    if len(states) > 0 and len(cities) > 0:
        # get all the places in a state
        cities_in_states = []
        for sid in states:
            from models.state import State
            state = storage.get(State, sid)
            for city_in_state in state.cities:
                cities_in_states.append(city_in_state)
        places_in_city = []
        for city_in_state in cities_in_states:
            for place in city_in_state.places:
                places_in_city.append(place.to_dict())

        places_in_state = [place for place in places_in_city]

        # get all places in a city
        places = []
        places_in_cities = []
        for cid in cities:
            from models.city import City
            city = storage.get(City, cid)
            for place_in_city in city.places:
                places_in_cities.append(place_in_city.to_dict())

        places_in_city = [place for place in places_in_cities]
        places_cities_states = places_in_state + places_in_city
        return jsonify(places_cities_states), 200

    return jsonify({}), 200
