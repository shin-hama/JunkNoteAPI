
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
MYSQL_PORT: str = config("MYSQL_PORT")
MYSQL_USER: str = config("MYSQL_USER")

PROJECT_NAME: str = config("PROJECT_NAME", default="Junk Note API")

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
