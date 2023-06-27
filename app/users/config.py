from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ENCODING: str

    class Config:
        env_file = ".env"


settings = Settings()

