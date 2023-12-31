from typing import Literal

from pydantic import BaseSettings, root_validator
from sqlalchemy import NullPool


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    LOG_LEVEL: Literal["INFO", "DEBUG", "PROD"]
    SENTRY_ACCESS: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    JWT_SECRET: str
    JWT_ENCODING: str

    REDIS_HOST: str
    REDIS_PORT: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    @root_validator
    def get_database_url(cls, v):
        v["DATABASE_URL"] = (
            f"postgresql+asyncpg://"
            f"{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:"
            f"{v['DB_PORT']}/{v['DB_NAME']}"
        )
        return v

    @root_validator
    def get_test_database_url(cls, v):
        v["TEST_DATABASE_URL"] = (
            f"postgresql+asyncpg://"
            f"{v['TEST_DB_USER']}:{v['TEST_DB_PASS']}@{v['TEST_DB_HOST']}:"
            f"{v['TEST_DB_PORT']}/{v['TEST_DB_NAME']}"
        )
        return v

    class Config:
        env_file = ".env"


settings = Settings()

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}
