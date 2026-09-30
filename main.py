from pydantic_ai import Agent
from pydantic_ai.providers import openai
from pydantic_ai_harness import Coder, Advisor
from pydantic_ai.capabilities import WebSearch

agent= Agent(capabilities=[
    Coder(),
    WebSearch(),
    Advisor()
])

agent.to_cli_sync()