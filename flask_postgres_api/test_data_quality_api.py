#!/usr/bin/env python3
# Data Quality API Testing Script
# Tests the data quality validation endpoints
 

import requests
import json
import time
from datetime import datetime

def test_data_quality_status():
    """Test the data quality status endpoint"""
    print("\n" + "="*60)
    print("TESTING DATA QUALITY STATUS ENDPOINT")
    print("="*60)

    try:
        response = requests.get('http://localhost:5000/data-quality/status')
        response.raise_for_status()

        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Timestamp: {data['timestamp']}")
        print(f"Total Courses: {data['summary']['total_courses']}")
        print(f"Total Users: {data['summary']['total_users']}")
        print(".2f")
        print(".2f")
        print(".2f")
        print(f"Recommendations: {len(data['recommendations'])} items")

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect: {str(e)}")
        print("Make sure the Flask server is running on http://localhost:5000")
        return False

def test_course_validation():
    """Test course data validation endpoint"""
    print("\n" + "="*60)
    print("TESTING COURSE DATA VALIDATION ENDPOINT")
    print("="*60)

    try:
        response = requests.get('http://localhost:5000/data-quality/courses')
        response.raise_for_status()

        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Table: {data['table']}")
        print(f"Timestamp: {data['validation_timestamp']}")
        print(f"Total Rows: {data['total_rows']}")
        print(".2f")
        print(f"Total Validations: {data['summary']['total_checks']}")
        print(f"Passed: {data['summary']['passed_checks']}")
        print(f"Failed: {data['summary']['failed_checks']}")
        print(f"Critical Failures: {data['summary']['critical_failures']}")
        print(f"Warning Failures: {data['summary']['warning_failures']}")

        # Show some validation details
        print("\nValidation Details:")
        for validation in data['validations'][:3]:  # Show first 3
            status = "✅" if validation['failed_rows'] == 0 else "❌"
            severity = "🔴" if validation['severity'] == 'critical' else "🟡"
            print(f"  {status} {severity} {validation['name']}: {validation['passed_rows']} passed, {validation['failed_rows']} failed")

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed: {str(e)}")
        return False

def test_user_validation():
    """Test user data validation endpoint"""
    print("\n" + "="*60)
    print("TESTING USER DATA VALIDATION ENDPOINT")
    print("="*60)

    try:
        response = requests.get('http://localhost:5000/data-quality/users')
        response.raise_for_status()

        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Table: {data['table']}")
        print(f"Timestamp: {data['validation_timestamp']}")
        print(f"Total Rows: {data['total_rows']}")
        print(".2f")
        print(f"Total Validations: {data['summary']['total_checks']}")
        print(f"Passed: {data['summary']['passed_checks']}")
        print(f"Failed: {data['summary']['failed_checks']}")

        # Show failed validations
        failed = [v for v in data['validations'] if v['failed_rows'] > 0]
        if failed:
            print(f"\nFailed Validations ({len(failed)}):")
            for validation in failed:
                severity = "🔴" if validation['severity'] == 'critical' else "🟡"
                print(f"  {severity} {validation['name']}: {validation['failed_rows']} failures")
        else:
            print("\n✅ All validations passed!")

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed: {str(e)}")
        return False

def test_comprehensive_validation():
    """Test comprehensive data validation endpoint"""
    print("\n" + "="*60)
    print("TESTING COMPREHENSIVE DATA VALIDATION ENDPOINT")
    print("="*60)

    try:
        response = requests.get('http://localhost:5000/data-quality/comprehensive')
        response.raise_for_status()

        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Timestamp: {data['timestamp']}")
        print(f"Tables Validated: {len(data['tables'])}")
        print(".2f")

        for table in data['tables']:
            status = "✅" if table['results']['quality_score'] >= 80 else "⚠️" if table['results']['quality_score'] >= 60 else "❌"
            print(f"  {status} {table['table']}: {table['results']['total_rows']} rows, {table['results']['quality_score']:.2f}% quality")

        overall_score = data['overall_quality_score']
        if overall_score >= 90:
            print("🎉 OVERALL: Excellent data quality!")
        elif overall_score >= 75:
            print("✅ OVERALL: Good data quality")
        elif overall_score >= 60:
            print("⚠️ OVERALL: Data quality needs attention")
        else:
            print("❌ OVERALL: Data quality requires improvement")

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed: {str(e)}")
        return False

def save_test_results(results):
    """Save test results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"api_test_results_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump({
            "test_timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)

    print(f"\n📄 Test results saved to: {filename}")

def main():
    """Main testing function"""
    print("Data Quality API Testing Script")
    print("This script tests all data quality validation endpoints")
    print("Make sure your Flask server is running on http://localhost:5000")
    print()

    # Wait a moment for user to start server if needed
    print("Starting tests in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    # Run all tests
    test_results = {}

    test_results['status'] = test_data_quality_status()
    test_results['courses'] = test_course_validation()
    test_results['users'] = test_user_validation()
    test_results['comprehensive'] = test_comprehensive_validation()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(test_results.values())
    total = len(test_results)

    print(f"Tests Passed: {passed}/{total}")

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("Data quality API is working correctly.")
    else:
        print("⚠️ Some tests failed.")
        print("Check the output above for details.")

    # Save results
    save_test_results(test_results)

    print("\nAvailable endpoints:")
    print("- GET /data-quality/status")
    print("- GET /data-quality/courses")
    print("- GET /data-quality/users")
    print("- GET /data-quality/comprehensive")

if __name__ == "__main__":
    main()
