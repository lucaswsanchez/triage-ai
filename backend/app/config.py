"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com"
    llm_model: str = "deepseek-flash"
    llm_max_tokens: int = 700
    llm_temperature: float = 0.2
    llm_timeout_seconds: float = 30.0

    rate_limit_requests: int = 10
    rate_limit_window_seconds: int = 3600
    max_ticket_chars: int = 4000
    retrieval_top_k: int = 3

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    kb_site_url: str = "https://lucaswsanchez.github.io/helpdesk-kb"

    @property
    def llm_enabled(self) -> bool:
        return bool(self.llm_api_key.strip())

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
