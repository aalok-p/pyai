import os

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai_harness import Coder
from pydantic_ai.capabilities import WebSearch, WebFetch
from pydantic_ai.capabilities import LocalWorkspace

from pyai.config import Config
from pyai.providers import resolve_model


def main():
    config = Config.load()

    if config.providers:
        model = resolve_model(config, os.getenv("MODEL_NAME"))
    else:
        model = OpenAIChatModel(
            os.getenv("MODEL_NAME"),
            provider=OpenAIProvider(
                base_url=os.getenv("BASE_URL"),
                api_key=os.getenv("API_KEY"),
            ),
        )

    agent = Agent(
        model,
        capabilities=[
            LocalWorkspace("."),
            Coder(),
            WebSearch(),
            WebFetch(local=True),
        ],
    )
    agent.to_cli_sync()


if __name__ == "__main__":
    main()
