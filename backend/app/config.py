from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_url: str
    supabase_key: str
    anthropic_api_key: str | None = None
    app_env: str = "development"


settings = Settings()  # type: ignore[call-arg]
