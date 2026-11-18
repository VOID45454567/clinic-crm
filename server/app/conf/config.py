from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_TTL_MIN: int = 60
    REFRESH_TOKEN_TTL_DAYS: int = 7
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    ENV: str = "dev"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
