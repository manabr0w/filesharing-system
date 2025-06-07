from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "SharALL"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str

    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_BUCKET_NAME: str
    AWS_REGION: str = "eu-north-1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
