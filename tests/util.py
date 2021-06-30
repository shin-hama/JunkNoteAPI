import os

import pymysql

TEST_MYSQL_DATABASE = "test_db"
TEST_MYSQL_USER = "mysql"
TEST_MYSQL_PASSWORD = "mysql"
TEST_MYSQL_PORT = "3306"
# Connect to container is outside of this container
TEST_MYSQL_HOST = os.getenv("TEST_MYSQL_HOST", "host.docker.internal")

TEST_DB_URL = (
    f"mysql+pymysql://{TEST_MYSQL_USER}:{TEST_MYSQL_PASSWORD}"
    f"@{TEST_MYSQL_HOST}:{TEST_MYSQL_PORT}/{TEST_MYSQL_DATABASE}"
)
# Set Environment arg to read test database path in app
os.environ["DATABASE_URL"] = TEST_DB_URL


def is_database_ready() -> bool:
    """ Return True when success to connect mysql database.

    Return
    ------
    is_connected : bool
    """
    try:
        pymysql.connect(
            host=TEST_MYSQL_HOST,
            user=TEST_MYSQL_USER,
            password=TEST_MYSQL_PASSWORD,
            db=TEST_MYSQL_DATABASE,
        )
        return True
    except Exception:
        return False
