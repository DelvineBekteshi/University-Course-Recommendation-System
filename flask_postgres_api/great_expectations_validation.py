#!/usr/bin/env python3
# Great Expectations Data Quality Validation Script
# Runs comprehensive data quality checks using Great Expectations framework
 
import sys
import os
import json
from datetime import datetime
import pandas as pd

# Add the flask_postgres_api directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.great_expectations_validator import (
    CourseDataValidator,
    UserDataValidator,
    run_comprehensive_data_quality_check
)

# Database configuration
DB_CONFIG = {
    "dbname": "university_recommendations",
    "user": "user_admin",
    "password": "password123",
    "host": "localhost",
    "port": "5432"
}

def get_connection_string():
    """Generate PostgreSQL connection string"""
    return f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

def validate_courses():
    """Validate course data using Great Expectations"""
    print("\n" + "="*80)
    print("GREAT EXPECTATIONS - COURSE DATA VALIDATION")
    print("="*80)

    try:
        connection_string = get_connection_string()
        df = pd.read_sql("SELECT * FROM courses WHERE is_deleted = FALSE", connection_string)

        if len(df) == 0:
            print("No course data found to validate.")
            return

        print(f"Loaded {len(df)} courses for validation...")

        # Validate using Great Expectations
        validator = CourseDataValidator()
        results = validator.validate_dataframe(df)

        # Generate and print report
        report = validator.generate_quality_report(results)
        print(report)

        # Save detailed results
        validator.save_validation_results(results, "course_quality_report.json")

    except Exception as e:
        print(f"Error validating course data: {str(e)}")
        import traceback
        traceback.print_exc()

def validate_users():
    """Validate user data using Great Expectations"""
    print("\n" + "="*80)
    print("GREAT EXPECTATIONS - USER DATA VALIDATION")
    print("="*80)

    try:
        connection_string = get_connection_string()
        df = pd.read_sql("SELECT * FROM users WHERE is_deleted = FALSE", connection_string)

        if len(df) == 0:
            print("No user data found to validate.")
            return

        print(f"Loaded {len(df)} users for validation...")

        # Validate using Great Expectations
        validator = UserDataValidator()
        results = validator.validate_dataframe(df)

        # Print summary
        print(f"Validation Timestamp: {results['timestamp']}")
        print(f"Total Users: {results['total_rows']}")
        print(".2f")
        print(f"Successful Expectations: {sum(1 for r in results['results'] if r['success'])}")
        print(f"Failed Expectations: {sum(1 for r in results['results'] if not r['success'])}")

        # Show failed expectations
        failed_results = [r for r in results['results'] if not r['success']]
        if failed_results:
            print("\nFAILED EXPECTATIONS:")
            print("-" * 50)
            for result in failed_results:
                print(f" {result['expectation_type']} on column '{result['column']}'")
                print(f"   Unexpected items: {result['unexpected_count']}")
        else:
            print("\n ALL EXPECTATIONS PASSED!")

        # Save results
        with open("user_quality_report.json", "w") as f:
            json.dump(results, f, indent=2)
        print("\nDetailed results saved to: user_quality_report.json")
    except Exception as e:
        print(f"Error validating user data: {str(e)}")
        import traceback
        traceback.print_exc()

def run_comprehensive_check():
    """Run comprehensive data quality check on all tables"""
    print("\n" + "="*80)
    print("COMPREHENSIVE DATA QUALITY CHECK")
    print("="*80)

    try:
        connection_string = get_connection_string()
        report = run_comprehensive_data_quality_check(connection_string)

        print(f"Check Timestamp: {report['timestamp']}")
        print(f"Tables Checked: {len(report['tables_checked'])}")
        print(".2f")
        print()

        for table in report['tables_checked']:
            if 'error' in table:
                print(f" {table['table_name']}: ERROR - {table['error']}")
            else:
                score = table['quality_score']
                status = "Excellent" if score >= 95 else "Warning" if score >= 80 else "Critical"
                print(f"{status} {table['table_name']}: {table['row_count']} rows, {score:.2f}% quality")

        # Save comprehensive report
        with open("comprehensive_quality_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print("\nComprehensive report saved to: comprehensive_quality_report.json")
    except Exception as e:
        print(f"Error running comprehensive check: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python great_expectations_validation.py [courses|users|comprehensive]")
        print("Examples:")
        print("  python great_expectations_validation.py courses")
        print("  python great_expectations_validation.py users")
        print("  python great_expectations_validation.py comprehensive")
        return

    command = sys.argv[1].lower()

    if command == "courses":
        validate_courses()
    elif command == "users":
        validate_users()
    elif command == "comprehensive":
        run_comprehensive_check()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: courses, users, comprehensive")

if __name__ == "__main__":
    main()
