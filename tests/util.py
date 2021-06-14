import pymysql

from app.core.config import (
    MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
)


def is_database_ready(docker_ip: str) -> bool:
    try:
        pymysql.connect(
            host=docker_ip,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DATABASE,
        )
        return True
    except Exception:
        return False
