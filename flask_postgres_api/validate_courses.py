# Batch data validation and cleansing script for courses.
# Validates all courses in the database and produces a comprehensive report.
# Includes data quality metrics and suggestions for fixes.
 
import psycopg2
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

DB_NAME = "university_recommendations"
DB_USER = "user_admin"
DB_PASSWORD = "password123"
DB_HOST = "localhost"
DB_PORT = "5432"

ALLOWED_CATEGORIES = [
    "Programming",
    "Data Science",
    "AI",
    "Cybersecurity",
    "Web Development",
    "Database",
    "Networking"
]

def generate_validation_report(courses):
    """Generate comprehensive validation report with statistics"""
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_courses": len(courses),
        "valid_courses": 0,
        "errors": [],
        "warnings": [],
        "quality_score": 0.0,
        "statistics": {
            "missing_titles": 0,
            "missing_descriptions": 0,
            "duplicate_titles": 0,
            "invalid_categories": 0,
            "short_descriptions": 0,
        }
    }
    
    seen_titles = set()
    
    for course in courses:
        course_id, title, category, description = course
        course_errors = []
        course_warnings = []
        
        # Validate title
        if not title or not title.strip():
            report["statistics"]["missing_titles"] += 1
            course_errors.append(f"Course ID {course_id}: Missing or empty title")
        else:
            if title in seen_titles:
                report["statistics"]["duplicate_titles"] += 1
                course_errors.append(f"Course ID {course_id}: Duplicate title '{title}'")
            else:
                seen_titles.add(title)
        
        # Validate category
        if not category or category not in ALLOWED_CATEGORIES:
            report["statistics"]["invalid_categories"] += 1
            course_warnings.append(
                f"Course ID {course_id}: Invalid category '{category}' "
                f"(allowed: {', '.join(ALLOWED_CATEGORIES)})"
            )
        
        # Validate description
        if not description or not description.strip():
            report["statistics"]["missing_descriptions"] += 1
            course_errors.append(f"Course ID {course_id}: Missing description")
        elif len(description.strip()) < 10:
            report["statistics"]["short_descriptions"] += 1
            course_warnings.append(
                f"Course ID {course_id}: Description too short "
                f"({len(description.strip())} chars, minimum 10)"
            )
        
        if course_errors:
            report["errors"].extend(course_errors)
        if course_warnings:
            report["warnings"].extend(course_warnings)
        else:
            if not course_errors:
                report["valid_courses"] += 1
    
    # Calculate quality score
    total_issues = len(report["errors"]) + len(report["warnings"])
    report["quality_score"] = (1 - (total_issues / max(len(courses), 1))) * 100
    
    return report


def validate_courses():
    """Main validation function"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, category, description FROM courses")
        courses = cursor.fetchall()

        print("\n" + "="*70)
        print("COURSE DATA VALIDATION REPORT")
        print("="*70 + "\n")

        report = generate_validation_report(courses)

        # Print summary
        print(f"Timestamp: {report['timestamp']}")
        print(f"Total Courses Analyzed: {report['total_courses']}")
        print(f"Valid Courses: {report['valid_courses']}")
        print(f"Quality Score: {report['quality_score']:.2f}%\n")

        # Print statistics
        print("DATA QUALITY STATISTICS:")
        print("-" * 70)
        stats = report["statistics"]
        print(f"  ✗ Missing titles: {stats['missing_titles']}")
        print(f"  ✗ Missing descriptions: {stats['missing_descriptions']}")
        print(f"  ⚠ Invalid categories: {stats['invalid_categories']}")
        print(f"  ⚠ Duplicate titles: {stats['duplicate_titles']}")
        print(f"  ⚠ Short descriptions: {stats['short_descriptions']}\n")

        # Print errors
        if report["errors"]:
            print("ERRORS (Critical Issues):")
            print("-" * 70)
            for error in report["errors"]:
                print(f"  ✗ {error}")
            print()

        # Print warnings
        if report["warnings"]:
            print("WARNINGS (Non-Critical Issues):")
            print("-" * 70)
            for warning in report["warnings"]:
                print(f"  ⚠ {warning}")
            print()

        # Print recommendations
        if report["errors"] or report["warnings"]:
            print("RECOMMENDATIONS:")
            print("-" * 70)
            if stats['missing_titles'] > 0:
                print("  • Add missing titles to courses")
            if stats['missing_descriptions'] > 0:
                print("  • Add descriptions to courses")
            if stats['invalid_categories'] > 0:
                print("  • Update invalid categories to allowed values")
            if stats['duplicate_titles'] > 0:
                print("  • Resolve duplicate course titles")
            if stats['short_descriptions'] > 0:
                print("  • Expand short descriptions (minimum 10 characters)")
            print()

        print("="*70)
        print("VALIDATION COMPLETE")
        print("="*70 + "\n")

        # Save report to JSON file
        with open('validation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to: validation_report.json\n")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error during validation: {str(e)}")
        raise

if __name__ == "__main__":
    validate_courses()