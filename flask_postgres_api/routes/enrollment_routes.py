from flask import Blueprint, jsonify, request
from extensions import db
from models.enrollment import Enrollment

enrollment_bp = Blueprint('enrollment_bp', __name__)

@enrollment_bp.route('/enrollments', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([enrollment.to_dict() for enrollment in enrollments])

@enrollment_bp.route('/enrollments', methods=['POST'])
def add_enrollment():
    data = request.get_json()

    new_enrollment = Enrollment(
        user_id=data['user_id'],
        course_id=data['course_id']
    )

    db.session.add(new_enrollment)
    db.session.commit()

    return jsonify(new_enrollment.to_dict()), 201