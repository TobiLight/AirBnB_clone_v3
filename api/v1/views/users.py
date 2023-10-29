#!/usr/bin/python3
"""
Create a new view for User objects that handles all default RESTFul
API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """
    Retrieves the list of all User objects.
    """
    users = [user.to_dict()
             for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route("/users/<path:user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object
    """
    from models.user import User
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<path:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes an User object
    """
    from models.user import User
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Creates an User
    """
    data_body = request.get_json(force=True, silent=True)
    if not data_body:
        abort(400, "Not a JSON")

    if 'name' not in data_body:
        abort(400, "Missing name")

    from models.user import User
    user = User(**data_body)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<path:user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a user object
    """
    from models.user import User
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    data_body = request.get_json(force=True, silent=True)

    if not data_body:
        abort(400, "Not a JSON")

    user.first_name = data_body.get("first_name", user.first_name)
    user.last_name = data_body.get("last_name", user.last_name)
    user.password = data_body.get("password", user.password)
    user.save()
    return jsonify(user.to_dict()), 200
