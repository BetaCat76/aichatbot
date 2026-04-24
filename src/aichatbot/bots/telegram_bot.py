import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from aichatbot.agents.weather_agent import WeatherAgent
from aichatbot.bots.base import BaseBot
from aichatbot.config import TelegramConfig

logger = logging.getLogger(__name__)


class TelegramBot(BaseBot):
    def __init__(self, telegram_config: TelegramConfig, agent: WeatherAgent) -> None:
        self._config = telegram_config
        self._agent = agent
        self._app = Application.builder().token(telegram_config.token).build()
        self._app.add_handler(CommandHandler("start", self._handle_start))
        self._app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))

    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message is None:
            return
        await update.message.reply_text(
            "👋 Hello! I'm an AI weather assistant. Ask me about the weather in any city!\n"
            "Example: 'What's the weather like in Tokyo?'"
        )

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message is None or update.message.text is None:
            return

        user_text = update.message.text
        logger.info("Received message from user %s: %s", update.effective_user, user_text)

        await update.message.chat.send_action("typing")

        response = await self._agent.run(user_text)
        await update.message.reply_text(response)

    async def start(self) -> None:
        logger.info("Starting Telegram bot...")
        await self._app.initialize()
        await self._app.start()
        await self._app.updater.start_polling()  # type: ignore[union-attr]
        logger.info("Telegram bot is running.")

    async def stop(self) -> None:
        logger.info("Stopping Telegram bot...")
        await self._app.updater.stop()  # type: ignore[union-attr]
        await self._app.stop()
        await self._app.shutdown()
        logger.info("Telegram bot stopped.")
