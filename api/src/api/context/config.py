from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Duku API"
    VERSION: str = "1.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_PASSWORD: Optional[str] = None

    class Config:
        env_file = "src/api/.env"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://postgres:{self.DATABASE_PASSWORD}@localhost:5432/duku"
        )


settings = Settings()