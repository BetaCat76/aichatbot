import os
from dataclasses import dataclass
from typing import Any

import yaml


@dataclass
class ServerConfig:
    name: str
    description: str


@dataclass
class TelegramConfig:
    token: str


@dataclass
class LLMConfig:
    provider: str
    model: str
    api_key: str
    temperature: float
    max_tokens: int


@dataclass
class WeatherConfig:
    api_key: str


@dataclass
class Config:
    server: ServerConfig
    telegram: TelegramConfig
    llm: LLMConfig
    weather: WeatherConfig


def _resolve_value(value: Any) -> Any:
    """Expand values that start with '$' from environment variables."""
    if isinstance(value, str) and value.startswith("$"):
        env_var = value[1:]
        return os.environ.get(env_var, value)
    return value


def _resolve_dict(data: dict) -> dict:
    """Recursively resolve env vars in a config dict."""
    return {k: _resolve_dict(v) if isinstance(v, dict) else _resolve_value(v) for k, v in data.items()}


def load_config(path: str) -> Config:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    raw = _resolve_dict(raw)

    server = ServerConfig(**raw["server"])
    telegram = TelegramConfig(**raw["telegram"])
    llm = LLMConfig(**raw["llm"])
    weather = WeatherConfig(**raw["weather"])

    return Config(server=server, telegram=telegram, llm=llm, weather=weather)
