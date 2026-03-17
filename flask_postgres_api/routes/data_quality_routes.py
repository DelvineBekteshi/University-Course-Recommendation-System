from flask import Blueprint, jsonify
from services.simplified_data_validator import (
    CourseDataValidator,
    UserDataValidator,
    run_comprehensive_validation
)
import pandas as pd
from extensions import db
from models.course import Course
from models.user import User

data_quality_bp = Blueprint('data_quality_bp', __name__)

@data_quality_bp.route('/data-quality/courses', methods=['GET'])
def validate_course_data():
    """Validate course data using simplified data quality validator"""
    try:
        courses = Course.query.all()
        data = [course.serialize() for course in courses]

        if not data:
            return jsonify({
                "message": "No course data found to validate",
                "quality_score": 0,
                "total_rows": 0
            }), 200

        df = pd.DataFrame(data)
        validator = CourseDataValidator()
        results = validator.validate_dataframe(df)

        return jsonify({
            "table": "courses",
            "validation_timestamp": results["timestamp"],
            "total_rows": results["total_rows"],
            "quality_score": results["quality_score"],
            "summary": results["summary"],
            "validations": results["validations"]
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Data quality validation failed: {str(e)}"
        }), 500

@data_quality_bp.route('/data-quality/users', methods=['GET'])
def validate_user_data():
    """Validate user data using simplified data quality validator"""
    try:
        users = User.query.all()
        data = [user.to_dict() for user in users]

        if not data:
            return jsonify({
                "message": "No user data found to validate",
                "quality_score": 0,
                "total_rows": 0
            }), 200

        df = pd.DataFrame(data)
        validator = UserDataValidator()
        results = validator.validate_dataframe(df)

        return jsonify({
            "table": "users",
            "validation_timestamp": results["timestamp"],
            "total_rows": results["total_rows"],
            "quality_score": results["quality_score"],
            "summary": results["summary"],
            "validations": results["validations"]
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Data quality validation failed: {str(e)}"
        }), 500

@data_quality_bp.route('/data-quality/comprehensive', methods=['GET'])
def comprehensive_data_quality():
    """Run comprehensive data quality check on all tables"""
    try:
        courses = Course.query.all()
        users = User.query.all()

        course_data = [course.serialize() for course in courses]
        user_data = [user.to_dict() for user in users]

        if not course_data and not user_data:
            return jsonify({
                "message": "No data found to validate",
                "overall_quality_score": 0,
                "tables_validated": 0
            }), 200

        course_df = pd.DataFrame(course_data) if course_data else pd.DataFrame()
        user_df = pd.DataFrame(user_data) if user_data else pd.DataFrame()

        results = run_comprehensive_validation(course_df, user_df)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({
            "error": f"Comprehensive validation failed: {str(e)}"
        }), 500

@data_quality_bp.route('/data-quality/status', methods=['GET'])
def data_quality_status():
    """Get current data quality status summary"""
    try:
        total_courses = Course.query.count()
        total_users = User.query.count()

        courses_with_descriptions = Course.query.filter(
            Course.description.isnot(None),
            Course.description != ""
        ).count()

        users_with_valid_emails = User.query.filter(
            User.email.like('%@%')
        ).count()

        course_quality = (courses_with_descriptions / total_courses * 100) if total_courses > 0 else 0
        user_quality = (users_with_valid_emails / total_users * 100) if total_users > 0 else 0

        return jsonify({
            "timestamp": pd.Timestamp.now().isoformat(),
            "summary": {
                "total_courses": total_courses,
                "total_users": total_users,
                "course_description_completeness": round(course_quality, 2),
                "user_email_validity": round(user_quality, 2),
                "overall_quality_indicator": round((course_quality + user_quality) / 2, 2)
            },
            "recommendations": [
                "Run full data quality validation for detailed analysis",
                "Check /data-quality/courses and /data-quality/users endpoints",
                "Use /data-quality/comprehensive for complete assessment"
            ]
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Status check failed: {str(e)}"
        }), 500
