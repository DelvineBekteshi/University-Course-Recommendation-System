# #!/usr/bin/env python3
# Data Quality API Integration Guide
# Demonstrates how to use the data quality validation endpoints

import requests
import json
from datetime import datetime

class DataQualityClient:
    """Client for interacting with the data quality validation API"""

    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def get_status(self):
        """Get quick data quality status overview"""
        try:
            response = requests.get(f"{self.base_url}/data-quality/status")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def validate_courses(self):
        """Get comprehensive course data validation report"""
        try:
            response = requests.get(f"{self.base_url}/data-quality/courses")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def validate_users(self):
        """Get comprehensive user data validation report"""
        try:
            response = requests.get(f"{self.base_url}/data-quality/users")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def validate_comprehensive(self):
        """Get comprehensive validation across all tables"""
        try:
            response = requests.get(f"{self.base_url}/data-quality/comprehensive")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


class DataQualityReportGenerator:
    """Generate human-readable reports from validation results"""

    @staticmethod
    def format_status_report(data):
        """Format status report"""
        if "error" in data:
            return f"Error: {data['error']}\n\nMake sure Flask server is running on http://localhost:5000"

        report = "\n" + "=" * 70
        report += "\nDATA QUALITY STATUS REPORT"
        report += "\n" + "=" * 70

        summary = data.get("summary", {})
        report += f"\nTimestamp: {data.get('timestamp', 'N/A')}"
        report += f"\n\nCourse Metrics:"
        report += f"\n  Total Courses: {summary.get('total_courses', 0)}"
        report += f"\n  Description Completeness: {summary.get('course_description_completeness', 0):.2f}%"
        report += f"\n\nUser Metrics:"
        report += f"\n  Total Users: {summary.get('total_users', 0)}"
        report += f"\n  Email Validity: {summary.get('user_email_validity', 0):.2f}%"
        report += f"\n\nOverall Quality: {summary.get('overall_quality_indicator', 0):.2f}%"

        if data.get("recommendations"):
            report += "\n\nRecommendations:"
            for rec in data["recommendations"]:
                report += f"\n  • {rec}"

        report += "\n" + "=" * 70 + "\n"
        return report

    @staticmethod
    def format_validation_report(data, table_name=""):
        """Format detailed validation report"""
        if "error" in data:
            return f"Error: {data['error']}"

        report = "\n" + "=" * 70
        report += f"\nDATA QUALITY REPORT - {data.get('table', table_name).upper()}"
        report += "\n" + "=" * 70

        report += f"\nValidation Timestamp: {data.get('validation_timestamp', 'N/A')}"
        report += f"\nTotal Rows: {data.get('total_rows', 0)}"
        report += f"\nQuality Score: {data.get('quality_score', 0):.2f}%"

        # Summary section
        summary = data.get("summary", {})
        report += "\n\nSUMMARY:"
        report += f"\n  Total Checks: {summary.get('total_checks', 0)}"
        report += f"\n  Passed: {summary.get('passed_checks', 0)}"
        report += f"\n  Failed: {summary.get('failed_checks', 0)}"
        report += f"\n  Critical Failures: {summary.get('critical_failures', 0)}"
        report += f"\n  Warning Failures: {summary.get('warning_failures', 0)}"

        # Quality assessment
        score = data.get('quality_score', 0)
        if score >= 90:
            assessment = " EXCELLENT - Data quality is outstanding"
        elif score >= 75:
            assessment = " GOOD - Data quality is acceptable"
        elif score >= 60:
            assessment = " NEEDS ATTENTION - Data quality requires review"
        else:
            assessment = " CRITICAL - Data quality requires immediate attention"

        report += f"\n\nAssessment: {assessment}"

        # Detailed validations
        validations = data.get("validations", [])
        if validations:
            report += "\n\nDETAILED VALIDATIONS:"
            report += "\n" + "-" * 70

            for val in validations:
                status = " PASSED" if val.get("failed_rows", 0) == 0 else " FAILED"
                severity = " CRITICAL" if val.get("severity") == "critical" else " WARNING"

                report += f"\n{status} {severity} - {val.get('name', 'Unknown')}"
                report += f"\n  Description: {val.get('description', 'N/A')}"
                report += f"\n  Results: {val.get('passed_rows', 0)} passed, {val.get('failed_rows', 0)} failed"

                if val.get("failed_rows", 0) > 0:
                    report += f"\n  Failure Rate: {val.get('failure_rate', 0):.1f}%"
                    if val.get("failed_examples"):
                        report += "\n  Failed Examples:"
                        for example in val.get("failed_examples", [])[:3]:
                            report += f"\n    • Row {example.get('row_index')}: {example.get('failed_value', 'N/A')}"

        report += "\n" + "=" * 70 + "\n"
        return report

    @staticmethod
    def format_comprehensive_report(data):
        """Format comprehensive validation report"""
        if "error" in data:
            return f"Error: {data['error']}"

        report = "\n" + "=" * 70
        report += "\nCOMPREHENSIVE DATA QUALITY ASSESSMENT"
        report += "\n" + "=" * 70

        report += f"\nTimestamp: {data.get('timestamp', 'N/A')}"
        report += f"\nTables Validated: {len(data.get('tables', []))}"
        report += f"\nOverall Quality Score: {data.get('overall_quality_score', 0):.2f}%"

        # Table-by-table results
        report += "\n\nTABLE RESULTS:"
        report += "\n" + "-" * 70

        for table in data.get("tables", []):
            table_name = table.get("table", "Unknown")
            results = table.get("results", {})

            score = results.get("quality_score", 0)
            status = "Excellent" if score >= 80 else "Warning" if score >= 60 else "Critical"

            report += f"\n{status} {table_name.upper()}: {results.get('total_rows', 0)} rows, {score:.2f}% quality"
            report += f"\n   Critical Failures: {results.get('summary', {}).get('critical_failures', 0)}"
            report += f"\n   Warning Failures: {results.get('summary', {}).get('warning_failures', 0)}"

        # Overall assessment
        overall_score = data.get("overall_quality_score", 0)
        if overall_score >= 90:
            assessment = " EXCELLENT - All tables have outstanding data quality!"
        elif overall_score >= 75:
            assessment = " GOOD - Overall data quality is acceptable"
        elif overall_score >= 60:
            assessment = " NEEDS ATTENTION - Data quality should be reviewed"
        else:
            assessment = " CRITICAL - Data quality requires immediate attention"

        report += f"\n\nOVERALL ASSESSMENT: {assessment}"
        report += "\n" + "=" * 70 + "\n"
        return report


def demo_api_endpoints():
    """Demonstrate API usage"""
    print("\n" + "=" * 70)
    print("DATA QUALITY API - INTEGRATION DEMO")
    print("=" * 70)
    print("\nThis demo shows how to use the data quality validation API.")
    print("The API provides real-time access to data quality metrics.")

    client = DataQualityClient()
    generator = DataQualityReportGenerator()

    # Demo 1: Status endpoint
    print("\n\n1. QUICK STATUS CHECK")
    print("-" * 70)
    print("Endpoint: GET /data-quality/status")
    print("\nUsage: client.get_status()")
    print("\nExample Response:")
    print("""
    {
      "timestamp": "2024-01-15T10:30:00",
      "summary": {
        "total_courses": 150,
        "total_users": 500,
        "course_description_completeness": 95.2,
        "user_email_validity": 98.1,
        "overall_quality_indicator": 96.7
      },
      "recommendations": [...]
    }
    """)

    # Demo 2: Course validation
    print("\n2. COURSE DATA VALIDATION")
    print("-" * 70)
    print("Endpoint: GET /data-quality/courses")
    print("\nUsage: client.validate_courses()")
    print("\nReturns: Detailed course data quality report")
    print("  • Validates all non-deleted courses")
    print("  • Checks title, category, description")
    print("  • Returns quality score and failure details")

    # Demo 3: User validation
    print("\n3. USER DATA VALIDATION")
    print("-" * 70)
    print("Endpoint: GET /data-quality/users")
    print("\nUsage: client.validate_users()")
    print("\nReturns: Detailed user data quality report")
    print("  • Validates all non-deleted users")
    print("  • Checks name, email, role")
    print("  • Returns quality score and failure details")

    # Demo 4: Comprehensive validation
    print("\n4. COMPREHENSIVE VALIDATION")
    print("-" * 70)
    print("Endpoint: GET /data-quality/comprehensive")
    print("\nUsage: client.validate_comprehensive()")
    print("\nReturns: Cross-table validation results")
    print("  • Validates courses and users together")
    print("  • Provides overall quality assessment")
    print("  • Identifies relationships and dependencies")

    # Integration examples
    print("\n\n" + "=" * 70)
    print("INTEGRATION EXAMPLES")
    print("=" * 70)

    print("\n\n1. FRONTEND INTEGRATION")
    print("-" * 70)
    print("""
    // JavaScript/React example
    async function getDataQualityStatus() {
      const response = await fetch('/data-quality/status');
      const data = await response.json();
      displayQualityMetrics(data.summary);
    }
    
    // Display quality indicator
    const qualityScore = data.summary.overall_quality_indicator;
    const statusColor = qualityScore >= 90 ? 'green' : 
                       qualityScore >= 75 ? 'yellow' : 'red';
    displayMetric('Data Quality', qualityScore, statusColor);
    """)

    print("\n2. BACKEND INTEGRATION")
    print("-" * 70)
    print("""
    # Python example - check quality before recommendations
    from services.simplified_data_validator import CourseDataValidator
    
    def get_recommendations(user_id):
        # First check data quality
        validator = CourseDataValidator()
        quality = validator.check_quality_score()
        
        if quality < 60:
            return {"error": "Data quality too low for recommendations"}
        
        # Proceed with recommendations
        return generate_recommendations(user_id)
    """)

    print("\n3. SCHEDULED VALIDATION")
    print("-" * 70)
    print("""
    # Schedule validation checks daily
    from apscheduler.schedulers.background import BackgroundScheduler
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=run_daily_validation,
        trigger="cron",
        hour=2,  # Run at 2 AM
        minute=0
    )
    scheduler.start()
    
    def run_daily_validation():
        results = comprehensive_validation()
        if results['overall_quality_score'] < 75:
            send_alert_email(results)
    """)

    print("\n4. MONITORING DASHBOARD")
    print("-" * 70)
    print("""
    # Create live quality dashboard
    - Display overall quality score
    - Show quality trends over time
    - List critical failures
    - Alert on quality degradation
    - Provide remediation actions
    """)

    # Setup instructions
    print("\n\n" + "=" * 70)
    print("SETUP TO TEST API")
    print("=" * 70)

    print("\n1. Start PostgreSQL database (via Docker):")
    print("   docker-compose up -d")

    print("\n2. Run database migrations (if needed):")
    print("   python -m flask db upgrade")

    print("\n3. Start Flask server:")
    print("   python app.py")

    print("\n4. Test endpoints:")
    print("   curl http://localhost:5000/data-quality/status")
    print("   curl http://localhost:5000/data-quality/courses")
    print("   curl http://localhost:5000/data-quality/users")
    print("   curl http://localhost:5000/data-quality/comprehensive")

    print("\n5. Or use the Python client:")
    print("""
    from data_quality_api_integration import DataQualityClient
    
    client = DataQualityClient()
    status = client.get_status()
    print(status)
    """)

    print("\n\n" + "=" * 70)
    print("RESPONSE FORMAT")
    print("=" * 70)

    print("\n\nAll endpoints return JSON with the following structure:")
    print("""
    {
      "table": "courses|users|comprehensive",
      "validation_timestamp": "ISO 8601 timestamp",
      "total_rows": <number>,
      "quality_score": <0-100>,
      "summary": {
        "total_checks": <number>,
        "passed_checks": <number>,
        "failed_checks": <number>,
        "critical_failures": <number>,
        "warning_failures": <number>
      },
      "validations": [
        {
          "name": "validation_name",
          "description": "Human-readable description",
          "severity": "critical|warning",
          "passed_rows": <number>,
          "failed_rows": <number>,
          "failure_rate": <0-100>,
          "failed_examples": [...]
        },
        ...
      ]
    }
    """)

    print("\n" + "=" * 70)
    print("DEMO COMPLETE!")
    print("=" * 70)
    print("\nFor more details, see DATA_QUALITY_GUIDE.md")
    print("\n")


if __name__ == "__main__":
    demo_api_endpoints()
