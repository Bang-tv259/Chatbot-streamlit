from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class ChatUIConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="chat_ui_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # llm client (gemini)
    gemini_api_key: str

    # search engine (exa.ai)
    search_engine_api_key: str


config = ChatUIConfig()
