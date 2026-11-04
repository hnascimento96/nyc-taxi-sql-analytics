"""Tests for src/spark_session.py.

These tests start a real local Spark session, so they take a few seconds.
"""

from spark_session import get_spark


def test_spark_session_uses_project_settings():
    # Act
    spark = get_spark()

    # Assert
    assert spark.conf.get("spark.driver.memory") == "4g"
    assert spark.conf.get("spark.sql.session.timeZone") == "UTC"


def test_spark_can_run_sql():
    # Arrange
    spark = get_spark()

    # Act
    result = spark.sql("SELECT 1 + 1 AS total")
    total = result.collect()[0]["total"]

    # Assert
    assert total == 2