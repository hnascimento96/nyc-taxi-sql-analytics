"""Shared SparkSession for the project.

Every script and notebook gets its session from get_spark(),
so the Spark settings live in one place.
"""

from pyspark.sql import SparkSession


def get_spark() -> SparkSession:
    # 1. Get the session builder
    builder = SparkSession.builder

    # 2. Name the application (shown in logs and in the Spark UI)
    builder = builder.appName("nyc-taxi-sql-analytics")

    # 3. Memory for Spark. In local mode this is the whole Spark heap.
    #    4g fits a laptop with 8 GB of RAM.
    builder = builder.config("spark.driver.memory", "4g")

    # 4. Interpret timestamps in UTC, so results are the same on any machine
    builder = builder.config("spark.sql.session.timeZone", "UTC")

    # 5. Start the session (or reuse one already running in this process)
    spark = builder.getOrCreate()
    return spark