from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Duku API"
    VERSION: str = "1.0"
    API_V1_STR: str = "/api/v1"


settings = Settings()