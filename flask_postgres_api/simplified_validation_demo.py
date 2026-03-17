#!/usr/bin/env python3
# Simplified Data Quality Validation Demo
# Demonstrates data quality validation concepts without complex dependencies


import pandas as pd
import json
from datetime import datetime
from services.simplified_data_validator import (
    CourseDataValidator,
    UserDataValidator,
    run_comprehensive_validation
)

def create_sample_course_data():
    """Create sample course data with intentional quality issues"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6],
        'title': [
            'Python Programming Basics',
            'Data Science Fundamentals',
            'AI Machine Learning',
            'Cybersecurity Essentials',
            'Web Development',
            ''  # Empty title (critical failure)
        ],
        'category': [
            'Programming',
            'Data Science',
            'AI',
            'Cybersecurity',
            'Web Development',
            'Invalid Category'  # Invalid category (warning)
        ],
        'description': [
            'Learn Python programming from scratch with hands-on projects.',
            'Comprehensive introduction to data science methodologies.',
            'Explore artificial intelligence and machine learning concepts.',
            'Understanding cybersecurity principles and best practices.',
            'Full-stack web development with modern frameworks.',
            'Short'  #  Too short (< 10 chars) (warning)
        ],
        'is_deleted': [False, False, False, False, False, False]
    })

def create_sample_user_data():
    """Create sample user data with intentional quality issues"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['John', 'Jane', 'Bob', 'Alice'],
        'last_name': ['Doe', 'Smith', 'Johnson', 'Williams'],
        'email': [
            'john.doe@example.com',
            'jane.smith@example.com',
            'bob.johnson@example.com',
            'invalid-email'  #  Invalid email format (critical)
        ],
        'role': ['student', 'admin', 'instructor', 'invalid_role'],  #  Invalid role (warning)
        'is_deleted': [False, False, False, False]
    })

def demo_course_validation():
    """Demonstrate course data validation"""
    print("\n" + "="*80)
    print("DATA QUALITY VALIDATION - COURSE DATA")
    print("="*80)

    # Create sample data
    df = create_sample_course_data()
    print(f"Created sample dataset with {len(df)} courses")
    print("\nSample data (with intentional quality issues):")
    print(df.to_string(index=False))
    print("\nIssues in data:")
    print("• Row 6: Empty title (critical)")
    print("• Row 6: Invalid category (warning)")
    print("• Row 6: Description too short (warning)")
    print()

    # Validate using our validator
    validator = CourseDataValidator()
    results = validator.validate_dataframe(df)

    # Print results
    print(f"Validation Results:")
    print(f"- Total Rows: {results['total_rows']}")
    print(".2f")
    print(f"- Total Validations: {results['summary']['total_checks']}")
    print(f"- Passed Validations: {results['summary']['passed_checks']}")
    print(f"- Failed Validations: {results['summary']['failed_checks']}")
    print(f"- Critical Failures: {results['summary']['critical_failures']}")
    print(f"- Warning Failures: {results['summary']['warning_failures']}")
    print()

    # Show detailed results
    print("Detailed Validation Results:")
    print("-" * 60)

    for validation in results["validations"]:
        status = " PASSED" if validation["failed_rows"] == 0 else " FAILED"
        severity = " CRITICAL" if validation["severity"] == "critical" else " WARNING"

        print(f"{status} {severity} - {validation['name']}")
        print(f"  {validation['description']}")
        print(f"  Results: {validation['passed_rows']} passed, {validation['failed_rows']} failed ({validation['failure_rate']:.1f}%)")

        if validation["failed_examples"]:
            print("  Failed examples:")
            for example in validation["failed_examples"]:
                print(f"    Row {example['row_index']}: {example.get('failed_value', 'N/A')}")

        print()

    # Generate and save report
    report = validator.generate_report(results)
    print("QUALITY REPORT:")
    print(report)

    # Save results
    validator.save_results(results, "demo_course_quality_report.json")
    print("Detailed results saved to: demo_course_quality_report.json")

def demo_user_validation():
    """Demonstrate user data validation"""
    print("\n" + "="*80)
    print("DATA QUALITY VALIDATION - USER DATA")
    print("="*80)

    # Create sample data
    df = create_sample_user_data()
    print(f"Created sample dataset with {len(df)} users")
    print("\nSample data (with intentional quality issues):")
    print(df.to_string(index=False))
    print("\nIssues in data:")
    print("• Row 4: Invalid email format (critical)")
    print("• Row 4: Invalid role (warning)")
    print()

    # Validate using our validator
    validator = UserDataValidator()
    results = validator.validate_dataframe(df)

    # Print results
    print(f"Validation Results:")
    print(f"- Total Rows: {results['total_rows']}")
    print(".2f")
    print(f"- Passed Validations: {results['summary']['passed_checks']}")
    print(f"- Failed Validations: {results['summary']['failed_checks']}")
    print()

    # Show failed validations
    failed_validations = [v for v in results["validations"] if v["failed_rows"] > 0]
    if failed_validations:
        print("Failed Validations:")
        for validation in failed_validations:
            severity = " CRITICAL" if validation["severity"] == "critical" else " WARNING"
            print(f"{severity} {validation['name']}: {validation['failed_rows']} failures")

    print()

    # Save results
    validator.save_results(results, "demo_user_quality_report.json")
    print("Results saved to: demo_user_quality_report.json")

def demo_comprehensive_validation():
    """Demonstrate comprehensive validation across multiple tables"""
    print("\n" + "="*80)
    print("COMPREHENSIVE DATA QUALITY ASSESSMENT")
    print("="*80)

    # Create sample data for both tables
    course_df = create_sample_course_data()
    user_df = create_sample_user_data()

    # Run comprehensive validation
    results = run_comprehensive_validation(course_df, user_df)

    print(f"Comprehensive Check Timestamp: {results['timestamp']}")
    print(f"Tables Validated: {len(results['tables'])}")
    print(".2f")
    print()

    for table_result in results["tables"]:
        table_name = table_result["table"]
        table_data = table_result["results"]

        status = "Excellent" if table_data["quality_score"] >= 80 else "Warning" if table_data["quality_score"] >= 60 else "Critical"
        print(f"{status} {table_name}: {table_data['total_rows']} rows, {table_data['quality_score']:.2f}% quality")
        print(f"   Critical failures: {table_data['summary']['critical_failures']}")
        print(f"   Warning failures: {table_data['summary']['warning_failures']}")

    print()

    # Overall assessment
    overall_score = results["overall_quality_score"]
    if overall_score >= 90:
        print(" OVERALL: Excellent data quality across all tables!")
    elif overall_score >= 75:
        print(" OVERALL: Good data quality with minor issues")
    elif overall_score >= 60:
        print(" OVERALL: Data quality needs attention")
    else:
        print(" OVERALL: Data quality requires significant improvement")

    print()

    # Save comprehensive report
    with open("demo_comprehensive_quality_report.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Comprehensive report saved to: demo_comprehensive_quality_report.json")

def main():
    """Main demo function"""
    print("Data Quality Validation Demo")
    print("This demo shows data quality validation concepts")
    print("using sample data with intentional quality issues")
    print()

    try:
        demo_course_validation()
        demo_user_validation()
        demo_comprehensive_validation()

        print("\n" + "="*80)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("Generated files:")
        print("- demo_course_quality_report.json")
        print("- demo_user_quality_report.json")
        print("- demo_comprehensive_quality_report.json")
        print()
        print("Key concepts demonstrated:")
        print("• Declarative data quality rules")
        print("• Critical vs warning validations")
        print("• Quality scoring and reporting")
        print("• Failure analysis and examples")
        print("• Multi-table validation")

    except Exception as e:
        print(f"Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
