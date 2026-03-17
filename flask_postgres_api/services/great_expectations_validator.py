import pandas as pd
import great_expectations as ge
from great_expectations.expectations.expectation_configuration import ExpectationConfiguration
from great_expectations.core import ExpectationSuite
from great_expectations.validator.validator import Validator
from typing import Dict, List, Any
import json
from datetime import datetime
import os

class CourseDataValidator:
    """Data Quality Validator for Course data using Great Expectations"""

    def __init__(self):
        self.expectation_suite = ExpectationSuite(
            name="course_data_quality_suite",
            meta={"notes": "Data quality expectations for university courses"}
        )
        self._build_expectations()

    def _build_expectations(self):
        """Build comprehensive expectation suite for course data"""

        # Title expectations
        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_not_be_null",
                kwargs={"column": "title"}
            )
        )

        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_value_lengths_to_be_between",
                kwargs={
                    "column": "title",
                    "min_value": 3,
                    "max_value": 255
                }
            )
        )

        # Category expectations
        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_not_be_null",
                kwargs={"column": "category"}
            )
        )

        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_be_in_set",
                kwargs={
                    "column": "category",
                    "value_set": [
                        "Programming", "Data Science", "AI", "Cybersecurity",
                        "Web Development", "Database", "Networking"
                    ]
                }
            )
        )

        # Description expectations
        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_not_be_null",
                kwargs={"column": "description"}
            )
        )

        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_value_lengths_to_be_between",
                kwargs={
                    "column": "description",
                    "min_value": 10,
                    "max_value": 5000
                }
            )
        )

        # ID expectations
        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_be_unique",
                kwargs={"column": "id"}
            )
        )

        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_be_of_type",
                kwargs={
                    "column": "id",
                    "type_": "INTEGER"
                }
            )
        )

        # Soft delete flag
        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_be_in_set",
                kwargs={
                    "column": "is_deleted",
                    "value_set": [True, False]
                }
            )
        )

    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate a pandas DataFrame against the expectation suite

        Args:
            df: DataFrame containing course data

        Returns:
            Validation results dictionary
        """
        # Convert to Great Expectations DataFrame
        ge_df = ge.from_pandas(df)

        # Run validation
        results = ge_df.validate(expectation_suite=self.expectation_suite)

        # Process results
        validation_results = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_rows": len(df),
            "total_expectations": len(results.results),
            "successful_expectations": sum(1 for r in results.results if r.success),
            "failed_expectations": sum(1 for r in results.results if not r.success),
            "success_rate": results.success_percent,
            "results": []
        }

        for result in results.results:
            expectation_result = {
                "expectation_type": result.expectation_config.expectation_type,
                "column": result.expectation_config.kwargs.get("column", "N/A"),
                "success": result.success,
                "unexpected_count": result.result.get("unexpected_count", 0),
                "unexpected_percent": result.result.get("unexpected_percent", 0.0),
                "partial_unexpected_list": result.result.get("partial_unexpected_list", [])[:10]  # First 10 examples
            }
            validation_results["results"].append(expectation_result)

        return validation_results

    def validate_from_database(self, connection_string: str, table_name: str = "courses") -> Dict[str, Any]:
        """
        Validate data directly from database

        Args:
            connection_string: Database connection string
            table_name: Table to validate

        Returns:
            Validation results
        """
        # Read data from database
        df = pd.read_sql(f"SELECT * FROM {table_name} WHERE is_deleted = FALSE", connection_string)

        # Validate
        return self.validate_dataframe(df)

    def generate_quality_report(self, validation_results: Dict[str, Any]) -> str:
        """
        Generate a human-readable quality report

        Args:
            validation_results: Results from validate_dataframe()

        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 80)
        report.append("GREAT EXPECTATIONS DATA QUALITY REPORT")
        report.append("=" * 80)
        report.append("")

        report.append(f"Validation Timestamp: {validation_results['timestamp']}")
        report.append(f"Total Rows Analyzed: {validation_results['total_rows']}")
        report.append(f"Total Expectations: {validation_results['total_expectations']}")
        report.append(f"Successful Expectations: {validation_results['successful_expectations']}")
        report.append(f"Failed Expectations: {validation_results['failed_expectations']}")
        report.append(".2f")
        report.append("")

        if validation_results['failed_expectations'] > 0:
            report.append("FAILED EXPECTATIONS:")
            report.append("-" * 80)

            for result in validation_results['results']:
                if not result['success']:
                    report.append(f" {result['expectation_type']} on column '{result['column']}'")
                    report.append(f"   Unexpected items: {result['unexpected_count']} ({result['unexpected_percent']:.2f}%)")

                    if result['partial_unexpected_list']:
                        examples = result['partial_unexpected_list'][:5]
                        report.append(f"   Examples: {examples}")

                    report.append("")
        else:
            report.append(" ALL EXPECTATIONS PASSED!")
            report.append("Data quality is excellent.")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)

    def save_validation_results(self, results: Dict[str, Any], filename: str = "data_quality_report.json"):
        """
        Save validation results to JSON file

        Args:
            results: Validation results dictionary
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"Validation results saved to: {filename}")


class UserDataValidator:
    """Data Quality Validator for User data"""

    def __init__(self):
        self.expectation_suite = ExpectationSuite(
            name="user_data_quality_suite"
        )
        self._build_expectations()

    def _build_expectations(self):
        """Build expectations for user data"""

        # Email expectations
        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_not_be_null",
                kwargs={"column": "email"}
            )
        )

        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_be_unique",
                kwargs={"column": "email"}
            )
        )

        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_value_lengths_to_be_between",
                kwargs={
                    "column": "email",
                    "min_value": 5,
                    "max_value": 100
                }
            )
        )

        # Name expectations
        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_not_be_null",
                kwargs={"column": "name"}
            )
        )

        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_not_be_null",
                kwargs={"column": "last_name"}
            )
        )

        # Role expectations
        self.expectation_suite.add_expectation(
            ExpectationConfiguration(
                type="expect_column_values_to_be_in_set",
                kwargs={
                    "column": "role",
                    "value_set": ["student", "admin", "instructor"]
                }
            )
        )

    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate user DataFrame"""
        ge_df = ge.from_pandas(df)
        results = ge_df.validate(expectation_suite=self.expectation_suite)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_rows": len(df),
            "success_rate": results.success_percent,
            "results": [
                {
                    "expectation_type": r.expectation_config.expectation_type,
                    "column": r.expectation_config.kwargs.get("column", "N/A"),
                    "success": r.success,
                    "unexpected_count": r.result.get("unexpected_count", 0)
                }
                for r in results.results
            ]
        }


# Convenience functions
def validate_course_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Quick validation function for course data"""
    validator = CourseDataValidator()
    return validator.validate_dataframe(df)


def validate_user_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Quick validation function for user data"""
    validator = UserDataValidator()
    return validator.validate_dataframe(df)


def run_comprehensive_data_quality_check(connection_string: str) -> Dict[str, Any]:
    """
    Run comprehensive data quality check on all tables

    Args:
        connection_string: Database connection string

    Returns:
        Complete quality report
    """
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "tables_checked": [],
        "overall_quality_score": 0.0
    }

    tables_to_check = [
        ("courses", CourseDataValidator),
        ("users", UserDataValidator)
    ]

    total_score = 0
    checked_tables = 0

    for table_name, validator_class in tables_to_check:
        try:
            df = pd.read_sql(f"SELECT * FROM {table_name} WHERE is_deleted = FALSE", connection_string)

            if len(df) > 0:
                validator = validator_class()
                results = validator.validate_dataframe(df)

                table_report = {
                    "table_name": table_name,
                    "row_count": len(df),
                    "quality_score": results.get("success_rate", 0),
                    "validation_results": results
                }

                report["tables_checked"].append(table_report)
                total_score += results.get("success_rate", 0)
                checked_tables += 1

        except Exception as e:
            report["tables_checked"].append({
                "table_name": table_name,
                "error": str(e)
            })

    if checked_tables > 0:
        report["overall_quality_score"] = total_score / checked_tables

    return report
