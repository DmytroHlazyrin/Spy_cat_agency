from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
