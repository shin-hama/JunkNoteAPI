import logging

from starlette.config import Config
from starlette.datastructures import Secret

import app


VERSION: str = app.__version__

API_PREFIX: str = "/api"

TOKEN_PREFIX = "bearer"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

MYSQL_DATABASE: str = config("MYSQL_DATABASE", default="db")
MYSQL_HOST: str = config("MYSQL_HOST", default="localhost")
MYSQL_PASSWORD: str = config("MYSQL_PASSWORD", default="")
MYSQL_PORT: str = config("MYSQL_PORT", cast=int, default="3306")
MYSQL_USER: str = config("MYSQL_USER", default="")

DATABASE_URL = config(
    "DATABASE_URL",
    default=(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
)

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config("TOKEN_EXPIRE", cast=int, default=60)

PROJECT_NAME: str = config("PROJECT_NAME", default="Junk Note API")

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
