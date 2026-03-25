from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    database_url: str = "sqlite+aiosqlite:///./refbotka.db"

    # Consumed by botka.services.refinance_client.RefinanceClient
    refinance_api_url: str | None = None
    refinance_secret_key: str | None = None
    refinance_bot_entity_id: int | None = None

    # Consumed by botka.services.user_service.UserService (bootstrap admins)
    bootstrap_resident_ids: list[int] | str = []

    @field_validator("bootstrap_resident_ids", mode="before")
    @classmethod
    def parse_ids(cls, value: object) -> list[int]:
        if value is None:
            return []
        if isinstance(value, int):
            return [value]
        if isinstance(value, str):
            return [int(p) for p in value.split(",") if p.strip()]
        return list(value)  # type: ignore[arg-type]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="REFBOTKA_",
        case_sensitive=False,
    )
