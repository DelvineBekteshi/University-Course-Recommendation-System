from flask import Blueprint, request, jsonify
from extensions import db
from models.course import Course
from services.data_utils import sanitize_string, normalize_category
from services.audit_utils import log_audit

course_bp = Blueprint('course_bp', __name__)

ALLOWED_CATEGORIES = [
    "Programming",
    "Data Science",
    "AI",
    "Cybersecurity",
    "Web Development",
    "Database",
    "Networking"
]

@course_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.serialize() for course in courses])


@course_bp.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.serialize())


@course_bp.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()

    try:
        title = sanitize_string(data.get('title', ''), min_length=3, max_length=255)
        category = normalize_category(data.get('category', ''), ALLOWED_CATEGORIES)
        description = sanitize_string(data.get('description', ''), min_length=10, max_length=5000)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    existing_course = Course.query.filter_by(title=title).first()
    if existing_course:
        return jsonify({"error": "Course with this title already exists"}), 409

    new_course = Course(
        title=title,
        category=category,
        description=description
    )

    db.session.add(new_course)
    db.session.commit()

    log_audit(
        entity_type='Course',
        entity_id=new_course.id,
        action='CREATE',
        new_values=new_course.serialize(),
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )

    return jsonify(new_course.serialize()), 201


@course_bp.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()

    old_values = course.serialize()

    try:
        title = sanitize_string(
            data.get('title', course.title),
            min_length=3,
            max_length=255
        )
        category = normalize_category(
            data.get('category', course.category),
            ALLOWED_CATEGORIES
        )
        description = sanitize_string(
            data.get('description', course.description),
            min_length=10,
            max_length=5000
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    duplicate_course = Course.query.filter(
        Course.title == title,
        Course.id != id
    ).first()

    if duplicate_course:
        return jsonify({"error": "Another course with this title already exists"}), 409

    course.title = title
    course.category = category
    course.description = description

    db.session.commit()

    log_audit(
        entity_type='Course',
        entity_id=course.id,
        action='UPDATE',
        old_values=old_values,
        new_values=course.serialize(),
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )

    return jsonify(course.serialize())


@course_bp.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    log_audit(
        entity_type='Course',
        entity_id=course.id,
        action='DELETE',
        old_values=course.serialize(),
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )

    return jsonify({"message": "Course deleted successfully"})