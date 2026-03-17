import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Any

class SimpleDataValidator:
    """Simplified data quality validator without Great Expectations context requirements"""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.validations = []
        self._setup_validations()

    def _setup_validations(self):
        """Setup validation rules based on table type"""
        if self.table_name == "courses":
            self._setup_course_validations()
        elif self.table_name == "users":
            self._setup_user_validations()

    def _setup_course_validations(self):
        """Setup validations for course data"""
        self.validations = [
            {
                "name": "title_not_null",
                "description": "Title cannot be null or empty",
                "check": lambda row: bool(row.get('title') and str(row.get('title')).strip()),
                "severity": "critical"
            },
            {
                "name": "title_length",
                "description": "Title must be 3-255 characters",
                "check": lambda row: 3 <= len(str(row.get('title', ''))) <= 255,
                "severity": "critical"
            },
            {
                "name": "category_not_null",
                "description": "Category cannot be null",
                "check": lambda row: bool(row.get('category')),
                "severity": "critical"
            },
            {
                "name": "category_valid",
                "description": "Category must be from allowed list",
                "check": lambda row: row.get('category') in [
                    "Programming", "Data Science", "AI", "Cybersecurity",
                    "Web Development", "Database", "Networking"
                ],
                "severity": "warning"
            },
            {
                "name": "description_not_null",
                "description": "Description cannot be null or empty",
                "check": lambda row: bool(row.get('description') and str(row.get('description')).strip()),
                "severity": "critical"
            },
            {
                "name": "description_length",
                "description": "Description must be at least 10 characters",
                "check": lambda row: len(str(row.get('description', ''))) >= 10,
                "severity": "warning"
            },
            {
                "name": "is_deleted_boolean",
                "description": "is_deleted must be boolean",
                "check": lambda row: isinstance(row.get('is_deleted'), bool),
                "severity": "warning"
            }
        ]

    def _setup_user_validations(self):
        """Setup validations for user data"""
        self.validations = [
            {
                "name": "email_not_null",
                "description": "Email cannot be null or empty",
                "check": lambda row: bool(row.get('email') and str(row.get('email')).strip()),
                "severity": "critical"
            },
            {
                "name": "email_format",
                "description": "Email must contain @ and .",
                "check": lambda row: '@' in str(row.get('email', '')) and '.' in str(row.get('email', '')),
                "severity": "critical"
            },
            {
                "name": "name_not_null",
                "description": "Name cannot be null or empty",
                "check": lambda row: bool(row.get('name') and str(row.get('name')).strip()),
                "severity": "critical"
            },
            {
                "name": "last_name_not_null",
                "description": "Last name cannot be null or empty",
                "check": lambda row: bool(row.get('last_name') and str(row.get('last_name')).strip()),
                "severity": "critical"
            },
            {
                "name": "role_valid",
                "description": "Role must be student, admin, or instructor",
                "check": lambda row: row.get('role') in ["student", "admin", "instructor"],
                "severity": "warning"
            }
        ]

    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate DataFrame against defined rules

        Args:
            df: DataFrame to validate

        Returns:
            Validation results dictionary
        """
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "table_name": self.table_name,
            "total_rows": len(df),
            "validations": [],
            "summary": {
                "total_checks": 0,
                "passed_checks": 0,
                "failed_checks": 0,
                "critical_failures": 0,
                "warning_failures": 0
            }
        }

        # Convert DataFrame to list of dicts for easier processing
        rows = df.to_dict('records')

        for validation in self.validations:
            validation_result = {
                "name": validation["name"],
                "description": validation["description"],
                "severity": validation["severity"],
                "total_rows": len(rows),
                "passed_rows": 0,
                "failed_rows": 0,
                "failure_rate": 0.0,
                "failed_examples": []
            }

            for i, row in enumerate(rows):
                try:
                    if validation["check"](row):
                        validation_result["passed_rows"] += 1
                    else:
                        validation_result["failed_rows"] += 1
                        # Store first few examples of failures
                        if len(validation_result["failed_examples"]) < 3:
                            validation_result["failed_examples"].append({
                                "row_index": i,
                                "failed_value": row.get(list(row.keys())[0] if row else "N/A")  # First column value
                            })
                except Exception as e:
                    validation_result["failed_rows"] += 1
                    if len(validation_result["failed_examples"]) < 3:
                        validation_result["failed_examples"].append({
                            "row_index": i,
                            "error": str(e)
                        })

            validation_result["failure_rate"] = (validation_result["failed_rows"] / len(rows)) * 100

            results["validations"].append(validation_result)
            results["summary"]["total_checks"] += 1

            if validation_result["failed_rows"] == 0:
                results["summary"]["passed_checks"] += 1
            else:
                results["summary"]["failed_checks"] += 1
                if validation["severity"] == "critical":
                    results["summary"]["critical_failures"] += 1
                else:
                    results["summary"]["warning_failures"] += 1

        # Calculate overall quality score
        total_possible = results["summary"]["total_checks"] * len(rows)
        total_passed = sum(v["passed_rows"] for v in results["validations"])
        results["quality_score"] = (total_passed / total_possible * 100) if total_possible > 0 else 0

        return results

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable validation report"""
        report = []
        report.append("=" * 80)
        report.append(f"DATA QUALITY VALIDATION REPORT - {self.table_name.upper()}")
        report.append("=" * 80)
        report.append("")

        report.append(f"Validation Timestamp: {results['timestamp']}")
        report.append(f"Table: {results['table_name']}")
        report.append(f"Total Rows: {results['total_rows']}")
        report.append(".2f")
        report.append("")

        summary = results["summary"]
        report.append("SUMMARY:")
        report.append("-" * 50)
        report.append(f"Total Validations: {summary['total_checks']}")
        report.append(f"Passed Validations: {summary['passed_checks']}")
        report.append(f"Failed Validations: {summary['failed_checks']}")
        report.append(f"Critical Failures: {summary['critical_failures']}")
        report.append(f"Warning Failures: {summary['warning_failures']}")
        report.append("")

        # Quality assessment
        score = results["quality_score"]
        if score >= 95:
            report.append(" EXCELLENT: Data quality is outstanding!")
        elif score >= 80:
            report.append(" GOOD: Data quality is acceptable")
        elif score >= 60:
            report.append(" FAIR: Data quality needs attention")
        else:
            report.append(" POOR: Data quality requires immediate action")

        report.append("")

        # Detailed results
        report.append("DETAILED VALIDATION RESULTS:")
        report.append("-" * 50)

        for validation in results["validations"]:
            status = "Excellent" if validation["failed_rows"] == 0 else "Failed"
            severity_label = "CRITICAL" if validation["severity"] == "critical" else "WARNING"

            report.append(f"{status} [{severity_label}] {validation['name']}")
            report.append(f"   {validation['description']}")
            report.append(f"   Passed: {validation['passed_rows']}, Failed: {validation['failed_rows']} ({validation['failure_rate']:.1f}%)")

            if validation["failed_examples"]:
                report.append("   Examples of failures:")
                for example in validation["failed_examples"]:
                    report.append(f"     Row {example['row_index']}: {example.get('failed_value', example.get('error', 'N/A'))}")

            report.append("")

        report.append("=" * 80)

        return "\n".join(report)

    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save validation results to JSON file"""
        if filename is None:
            filename = f"{self.table_name}_quality_report.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"Results saved to: {filename}")


# Convenience classes
class CourseDataValidator(SimpleDataValidator):
    def __init__(self):
        super().__init__("courses")

class UserDataValidator(SimpleDataValidator):
    def __init__(self):
        super().__init__("users")


# Quick validation functions
def validate_course_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Quick validation for course data"""
    validator = CourseDataValidator()
    return validator.validate_dataframe(df)

def validate_user_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Quick validation for user data"""
    validator = UserDataValidator()
    return validator.validate_dataframe(df)

def run_comprehensive_validation(course_df: pd.DataFrame = None, user_df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Run comprehensive validation on both tables

    Args:
        course_df: Course data DataFrame (optional)
        user_df: User data DataFrame (optional)

    Returns:
        Combined validation results
    """
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "tables": []
    }

    if course_df is not None and len(course_df) > 0:
        course_validator = CourseDataValidator()
        course_results = course_validator.validate_dataframe(course_df)
        results["tables"].append({
            "table": "courses",
            "results": course_results
        })

    if user_df is not None and len(user_df) > 0:
        user_validator = UserDataValidator()
        user_results = user_validator.validate_dataframe(user_df)
        results["tables"].append({
            "table": "users",
            "results": user_results
        })

    # Calculate overall score
    if results["tables"]:
        total_score = sum(table["results"]["quality_score"] for table in results["tables"])
        results["overall_quality_score"] = total_score / len(results["tables"])
    else:
        results["overall_quality_score"] = 0

    return results
