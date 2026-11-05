"""Shared SparkSession for the project.

Every script and notebook gets its session from get_spark(),
so the Spark settings live in one place.
"""

from pyspark.sql import SparkSession


def get_spark() -> SparkSession:
    """Create or reuse the project's SparkSession.

    The session runs Spark in local mode (all CPU cores of this machine)
    with the settings shared by every script and notebook in the project:

    - spark.driver.memory = 4g: in local mode, the driver also runs the
      executors, so this is the whole Spark heap. Sized for 8 GB of RAM.
    - spark.sql.session.timeZone = UTC: time-zone-aware operations (for
      example current_timestamp() or columns of type timestamp) use UTC
      instead of the laptop's time zone, so results are the same on any
      machine. The TLC pickup/dropoff columns are timestamp_ntz (New York
      wall-clock time, no time zone), so this setting does not shift them.

    Returns:
        SparkSession: the active session, ready for spark.read and spark.sql.

    Notes:
        Driver memory is applied only when Spark starts. If a session is
        already running in this Python process (for example, in a notebook
        kernel), getOrCreate() returns that session unchanged. Restart the
        kernel for new settings to take effect.

    Example:
        >>> from spark_session import get_spark
        >>> spark = get_spark()
        >>> spark.sql("SELECT 1 AS ok").show()
    """
    # 1. Get the session builder.
    #    Its methods change the builder in place, so no reassignment is needed.
    builder = SparkSession.builder

    # 2. Name the application (shown in logs and in the Spark UI)
    builder.appName("nyc-taxi-sql-analytics")

    # 3. Memory for Spark. In local mode this is the whole Spark heap.
    #    4g fits a laptop with 8 GB of RAM.
    builder.config("spark.driver.memory", "4g")

    # 4. Use UTC for time-zone-aware operations, so results do not depend on
    #    the laptop's time zone (TLC timestamp_ntz columns are not affected)
    builder.config("spark.sql.session.timeZone", "UTC")

    # 5. Start the session (or reuse one already running in this process)
    spark = builder.getOrCreate()
    return spark