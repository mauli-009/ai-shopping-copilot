from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15        # was 30 — shorten it
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7           # NEW
    REDIS_URL: str = ""
    GROQ_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()