from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool
)
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# from agents import enable_verbose_stdout_logging

# enable_verbose_stdout_logging()

set_tracing_disabled(True)
# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Gemini (OpenAI-Compatible) Client
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model (Gemini)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",     # Model name you are using
    openai_client=client
)

agent = Agent(
    name="AI Assistant",
    instructions="""
You are an AI assistant that helps in answer questions.

""",
    model=model,
)

result = Runner.run_sync(
    agent,
    input="Hello",
)
print("AI Response:\n", result.final_output)
