from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, model_validator

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./soilwise.db"
    jwt_secret: str = "development-only-change-me"
    access_token_minutes: int = 30
    cors_origins: str = "http://localhost:3000"
    upload_dir: str = "uploads"
    max_upload_mb: int = 8
    sarvam_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("jwt_secret")
    @classmethod
    def validate_secret(cls, value: str, info):
        env = info.data.get("app_env", "development")
        if env == "production" and (len(value) < 32 or value in {"development-only-change-me", "replace-this-with-a-random-secret-of-at-least-32-characters"}):
            raise ValueError("JWT_SECRET must be a unique secret of at least 32 characters in production")
        return value

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.app_env == "production":
            if "*" in self.cors_origin_list:
                raise ValueError("Wildcard CORS origins are not allowed in production")
            if not self.cors_origin_list:
                raise ValueError("At least one explicit CORS origin is required in production")
            if self.max_upload_mb < 1 or self.max_upload_mb > 20:
                raise ValueError("MAX_UPLOAD_MB must be between 1 and 20")
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

settings = Settings()
