from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings

PROJECT_ROOT = Path(__file__).parents[2]


class Environment(BaseSettings):
    """ read .env
    """
    database_url: str
    mysql_root_password: str
    mysql_database: str
    mysql_user: str
    mysql_password: str
    mysql_host: str

    class Config:
        env_file = PROJECT_ROOT / '.env'


@lru_cache
def get_env():
    """ Get environment args and cache it by @lru_cache
    """
    return Environment()
