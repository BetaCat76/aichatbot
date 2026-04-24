import asyncio
import logging
import os
from pathlib import Path

from aichatbot.agents.weather_agent import create_weather_agent
from aichatbot.bots.telegram_bot import TelegramBot
from aichatbot.config import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _find_config() -> str:
    if env_path := os.environ.get("CONFIG_PATH"):
        return env_path
    # Walk up from this file to find config.yaml at project root
    candidates = [
        Path(__file__).parents[3] / "config.yaml",  # project root in src layout
        Path.cwd() / "config.yaml",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    raise FileNotFoundError("config.yaml not found. Set CONFIG_PATH env var or place config.yaml in the project root.")


def main() -> None:
    config_path = _find_config()
    logger.info("Loading config from: %s", config_path)
    config = load_config(config_path)

    agent = create_weather_agent(config)
    bot = TelegramBot(config.telegram, agent)

    async def run() -> None:
        await bot.start()
        try:
            # Keep running until interrupted
            await asyncio.Event().wait()
        finally:
            await bot.stop()

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("Shutting down...")


if __name__ == "__main__":
    main()
