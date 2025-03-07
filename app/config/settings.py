from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017/senama"
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OTP_EXPIRE_MINUTES: int = 5
    REFRESH_SECRET_KEY = "your-refresh-secret-key-here"

    class Config:
        env_file = ".env"


settings = Settings()
