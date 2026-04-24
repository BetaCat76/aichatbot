import logging

import pyowm
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from aichatbot.config import Config

logger = logging.getLogger(__name__)


def _make_get_weather_tool(api_key: str):
    @tool
    def get_weather(city: str) -> str:
        """Get the current weather for a given city name.

        Args:
            city: The name of the city to get weather for.

        Returns:
            A string describing the current weather conditions.
        """
        try:
            owm = pyowm.OWM(api_key)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(city)
            w = observation.weather

            temp_c = w.temperature("celsius")["temp"]
            feels_like_c = w.temperature("celsius")["feels_like"]
            description = w.detailed_status
            humidity = w.humidity
            wind_speed = w.wind()["speed"]

            return (
                f"Weather in {city}: {description}. "
                f"Temperature: {temp_c:.1f}°C (feels like {feels_like_c:.1f}°C). "
                f"Humidity: {humidity}%. "
                f"Wind speed: {wind_speed} m/s."
            )
        except pyowm.commons.exceptions.NotFoundError:
            return f"City '{city}' not found. Please check the city name."
        except pyowm.commons.exceptions.UnauthorizedError:
            return "Invalid OpenWeatherMap API key."
        except Exception as e:
            logger.error("Weather API error for city '%s': %s", city, e)
            return f"Could not retrieve weather data for '{city}'. Please try again later."

    return get_weather


def create_weather_agent(config: Config) -> "WeatherAgent":
    return WeatherAgent(config)


class WeatherAgent:
    def __init__(self, config: Config) -> None:
        self._config = config

        llm = ChatOpenAI(
            model=config.llm.model,
            api_key=config.llm.api_key,  # type: ignore[arg-type]
            temperature=config.llm.temperature,
            max_tokens=config.llm.max_tokens,
        )

        tools = [_make_get_weather_tool(config.weather.api_key)]

        self._graph = create_agent(
            llm,
            tools,
            system_prompt=(
                "You are a helpful weather assistant. Use the get_weather tool to answer weather questions. "
                "Always provide friendly, informative responses."
            ),
        )

    async def run(self, user_input: str) -> str:
        try:
            result = await self._graph.ainvoke({"messages": [HumanMessage(content=user_input)]})
            messages = result.get("messages", [])
            # Return the last AI message content
            for msg in reversed(messages):
                if isinstance(msg, AIMessage) and msg.content:
                    return str(msg.content)
            return "Sorry, I could not process your request."
        except Exception as e:
            logger.error("Agent error: %s", e)
            return "Sorry, an error occurred while processing your request."
