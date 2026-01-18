from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file: str = ".env"
        extra: str = "ignore"


settings = Settings()
