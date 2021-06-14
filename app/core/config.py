
import logging

from starlette.config import Config

import app

API_PREFIX: str = "/api"

VERSION: str = app.__version__

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

MYSQL_DATABASE: str = config("MYSQL_DATABASE")
MYSQL_HOST: str = config("MYSQL_HOST")
MYSQL_PASSWORD: str = config("MYSQL_PASSWORD")
MYSQL_PORT: str = config("MYSQL_PORT", cast=int)
MYSQL_USER: str = config("MYSQL_USER")

DATABASE_URL = config(
    "DATABASE_URL",
    default=(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
)

PROJECT_NAME: str = config("PROJECT_NAME", default="Junk Note API")

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
