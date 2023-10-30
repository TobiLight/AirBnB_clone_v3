#!/usr/bin/python3
"""
Create a new view for Review objects that handles all default RESTFul
API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/places/<path:place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def all_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.
    """
    from models.place import Place
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<path:review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object
    """
    from models.review import Review
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<path:review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object
    """
    from models.review import Review
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<path:place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review
    """
    from models.place import Place
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data_body = request.get_json(force=True, silent=True)

    if not data_body:
        abort(400, "Not a JSON")

    if 'user_id' not in data_body:
        abort(400, "Missing user_id")

    if 'text' not in data_body:
        abort(400, "Missing text")

    data_body['place_id'] = place_id
    from models.user import User
    user = storage.get(User, data_body['user_id'])

    if user is None:
        abort(404)

    from models.review import Review
    review = Review(**data_body)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<path:review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object
    """
    from models.review import Review
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    data_body = request.get_json(force=True, silent=True)

    if not data_body:
        abort(400, "Not a JSON")

    # for key, value in data_body.items():
    #     if key not in ["id", "user_id", "place_id", "created_at",
    #                    "updated_at"]:
    #         setattr(review, key, value)
    review.text = data_body.get("text", review.text)
    review.save()
    return jsonify(review.to_dict()), 200
