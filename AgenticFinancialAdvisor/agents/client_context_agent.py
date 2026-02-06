from agents import Agent
from langfuse.openai import OpenAI
from langfuse import observe
from config import OPENAI_API_KEY, MODEL_CHOICE

client = OpenAI(api_key=OPENAI_API_KEY)
model = MODEL_CHOICE

@observe(name="ClientContextAgent")
def create_client_context_agent():
    return Agent(
        name="ClientContextAgent",
        instructions="""
You are a Client Context Agent for a financial advisor.

Responsibilities:
- Summarize client profile, goals, risk tolerance, and life events
- Do NOT give investment advice
- Output concise bullet points
""",
        model=model
    )

client_context_agent = create_client_context_agent()