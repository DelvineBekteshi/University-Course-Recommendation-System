from flask import Blueprint, jsonify, request
from extensions import db
from models.rating import Rating

rating_bp = Blueprint('rating_bp', __name__)

@rating_bp.route('/ratings', methods=['GET'])
def get_ratings():
    ratings = Rating.query.all()
    return jsonify([rating.to_dict() for rating in ratings])

@rating_bp.route('/ratings', methods=['POST'])
def add_rating():
    data = request.get_json()

    new_rating = Rating(
        user_id=data['user_id'],
        course_id=data['course_id'],
        score=data['score']
    )

    db.session.add(new_rating)
    db.session.commit()

    return jsonify(new_rating.to_dict()), 201