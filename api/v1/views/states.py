#!/usr/bin/python3
"""
Create a new view for State objects that handles all default RESTFul
API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """
    Retrieves the list of all State objects
    """
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route("/states/<path:state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object
    """
    from models.state import State
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<path:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object
    """
    from models.state import State
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Creates a State
    """
    data_body = request.get_json(force=True, silent=True)
    if not data_body:
        abort(400, "Not a JSON")

    if 'name' not in data_body:
        abort(400, "Missing name")

    from models.state import State
    state = State(**data_body)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<path:state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object
    """
    from models.state import State
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    data_body = request.get_json(force=True, silent=True)

    if not data_body:
        abort(400, "Not a JSON")

    state.name = data_body.get("name", state.name)
    state.save()
    return jsonify(state.to_dict()), 200
