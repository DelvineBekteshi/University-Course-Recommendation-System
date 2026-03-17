#!/usr/bin/env python3
# Great Expectations Data Quality Validation Demo
# Demonstrates Great Expectations functionality with sample data

import pandas as pd
import json
from datetime import datetime
from services.great_expectations_validator import CourseDataValidator, UserDataValidator

def create_sample_course_data():
    """Create sample course data for demonstration"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6],
        'title': [
            'Python Programming Basics',
            'Data Science Fundamentals',
            'AI Machine Learning',
            'Cybersecurity Essentials',
            'Web Development',
            ''  # Invalid: empty title
        ],
        'category': [
            'Programming',
            'Data Science',
            'AI',
            'Cybersecurity',
            'Web Development',
            'Invalid Category'  # Invalid: not in allowed list
        ],
        'description': [
            'Learn Python programming from scratch with hands-on projects.',
            'Comprehensive introduction to data science methodologies.',
            'Explore artificial intelligence and machine learning concepts.',
            'Understanding cybersecurity principles and best practices.',
            'Full-stack web development with modern frameworks.',
            'Short'  # Invalid: too short (< 10 chars)
        ],
        'is_deleted': [False, False, False, False, False, False]
    })

def create_sample_user_data():
    """Create sample user data for demonstration"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['John', 'Jane', 'Bob', 'Alice'],
        'last_name': ['Doe', 'Smith', 'Johnson', 'Williams'],
        'email': [
            'john.doe@example.com',
            'jane.smith@example.com',
            'bob.johnson@example.com',
            'invalid-email'  # Invalid: not proper email format
        ],
        'role': ['student', 'admin', 'instructor', 'invalid_role'],  # Invalid: not in allowed roles
        'is_deleted': [False, False, False, False]
    })

def demo_course_validation():
    """Demonstrate course data validation"""
    print("\n" + "="*80)
    print("GREAT EXPECTATIONS - COURSE DATA VALIDATION DEMO")
    print("="*80)

    # Create sample data
    df = create_sample_course_data()
    print(f"Created sample dataset with {len(df)} courses")
    print("\nSample data:")
    print(df.to_string(index=False))
    print()

    # Validate using Great Expectations
    validator = CourseDataValidator()
    results = validator.validate_dataframe(df)

    # Print results
    print(f"Validation Results:")
    print(f"- Total Expectations: {results['total_expectations']}")
    print(f"- Successful: {results['successful_expectations']}")
    print(f"- Failed: {results['failed_expectations']}")
    print(".2f")
    print()

    # Show detailed results
    print("Detailed Results:")
    for result in results['results']:
        status = "Excellent" if result['success'] else "Failed"
        print(f"{status} {result['expectation_type']} on '{result['column']}': {result['unexpected_count']} unexpected")

        if not result['success'] and result['partial_unexpected_list']:
            print(f"   Examples: {result['partial_unexpected_list'][:3]}")

    print()

    # Generate and save report
    report = validator.generate_quality_report(results)
    print("Quality Report:")
    print(report)

    # Save results
    validator.save_validation_results(results, "demo_course_quality_report.json")
    print("Results saved to: demo_course_quality_report.json")

def demo_user_validation():
    """Demonstrate user data validation"""
    print("\n" + "="*80)
    print("GREAT EXPECTATIONS - USER DATA VALIDATION DEMO")
    print("="*80)

    # Create sample data
    df = create_sample_user_data()
    print(f"Created sample dataset with {len(df)} users")
    print("\nSample data:")
    print(df.to_string(index=False))
    print()

    # Validate using Great Expectations
    validator = UserDataValidator()
    results = validator.validate_dataframe(df)

    # Print results
    print(f"Validation Results:")
    print(f"- Total Expectations: {len(results['results'])}")
    print(f"- Successful: {sum(1 for r in results['results'] if r['success'])}")
    print(f"- Failed: {sum(1 for r in results['results'] if not r['success'])}")
    print(f"- Success Rate: {results['success_rate']:.2f}%")
    print()

    # Show detailed results
    print("Detailed Results:")
    for result in results['results']:
        status = "Excellent" if result['success'] else "Failed"
        print(f"{status} {result['expectation_type']} on '{result['column']}': {result['unexpected_count']} unexpected")

    print()

    # Save results
    with open("demo_user_quality_report.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Results saved to: demo_user_quality_report.json")

def demo_combined_validation():
    """Demonstrate combined validation with quality scoring"""
    print("\n" + "="*80)
    print("COMBINED DATA QUALITY ASSESSMENT")
    print("="*80)

    # Validate both datasets
    course_df = create_sample_course_data()
    user_df = create_sample_user_data()

    course_validator = CourseDataValidator()
    user_validator = UserDataValidator()

    course_results = course_validator.validate_dataframe(course_df)
    user_results = user_validator.validate_dataframe(user_df)

    # Calculate overall quality
    course_score = course_results['success_rate']
    user_score = user_results['success_rate']
    overall_score = (course_score + user_score) / 2

    print(f"Overall Data Quality Score: {overall_score:.2f}%")
    print(f"- Course Data Quality: {course_score:.2f}%")
    print(f"- User Data Quality: {user_score:.2f}%")
    print()

    # Quality assessment
    if overall_score >= 95:
        print(" EXCELLENT: Data quality is outstanding!")
    elif overall_score >= 80:
        print(" GOOD: Data quality is acceptable with minor issues")
    elif overall_score >= 60:
        print(" FAIR: Data quality needs attention")
    else:
        print(" POOR: Data quality requires immediate action")

    print()

    # Recommendations
    print("Recommendations:")
    if course_results['failed_expectations'] > 0:
        print("- Review course data for missing titles, invalid categories, and short descriptions")
    if user_results['failed_expectations'] > 0:
        print("- Review user data for invalid emails and roles")

    # Save combined report
    combined_report = {
        "timestamp": datetime.utcnow().isoformat(),
        "overall_quality_score": overall_score,
        "course_quality": course_results,
        "user_quality": user_results
    }

    with open("demo_combined_quality_report.json", "w") as f:
        json.dump(combined_report, f, indent=2)

    print("\nCombined report saved to: demo_combined_quality_report.json")

def main():
    """Main demo function"""
    print("Great Expectations Data Quality Validation Demo")
    print("This demo shows how Great Expectations validates data quality")
    print("using sample data (no database connection required)")
    print()

    try:
        demo_course_validation()
        demo_user_validation()
        demo_combined_validation()

        print("\n" + "="*80)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("Generated files:")
        print("- demo_course_quality_report.json")
        print("- demo_user_quality_report.json")
        print("- demo_combined_quality_report.json")
        print()
        print("To run validation on real database data:")
        print("1. Start PostgreSQL database (docker-compose up -d)")
        print("2. Run: python great_expectations_validation.py comprehensive")

    except Exception as e:
        print(f"Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
