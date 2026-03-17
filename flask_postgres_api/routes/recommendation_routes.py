from flask import Blueprint, jsonify, request
from models.recommendation import Recommendation
from services.recommendation_cache import get_cached_recommendations, set_cached_recommendations

recommendation_bp = Blueprint('recommendation_bp', __name__)

@recommendation_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    cached_data = get_cached_recommendations(user_id)

    if cached_data:
        return jsonify({
            "source": "redis_cache",
            "data": cached_data
        })

    recommendations = Recommendation.query.filter_by(user_id=user_id).all()
    result = [r.to_dict() for r in recommendations]

    set_cached_recommendations(user_id, result)

    return jsonify({
        "source": "postgresql",
        "data": result
    })