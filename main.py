from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai_harness import Coder, Advisor
from pydantic_ai.capabilities import WebSearch
from pydantic_ai.capabilities import LocalWorkspace
import os
from dotenv import load_dotenv

load_dotenv()

model = OpenAIResponsesModel(os.getenv('MODEL_NAME'), provider=OpenAIProvider(base_url=os.getenv('BASE_URL'), api_key=os.getenv('API_KEY')))
agent = Agent(model,capabilities=[
    LocalWorkspace('.'),
    Coder(),
    WebSearch(),
    Advisor('minimax-m2.5')
])

agent.to_cli_sync()