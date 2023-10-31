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
    all_places = [p for p in storage.all('Place').values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all('City')
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get('City', c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get('Amenity', a_id)])
        for p in all_places:
            p_amenities = None
            if STORAGE_TYPE == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
