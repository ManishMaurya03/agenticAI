from agents import Agent
from langfuse.openai import OpenAI
from langfuse import observe

from config import OPENAI_API_KEY, MODEL_CHOICE

client = OpenAI(api_key=OPENAI_API_KEY)
model = MODEL_CHOICE

@observe(name="MarketAnalysisAgent")
def create_market_agent():
    return Agent(
        name="MarketAnalysisAgent",
        instructions="""
You analyze client portfolios.

Responsibilities:
- Identify allocation, performance, and risk observations
- Highlight concentration or drift
- Do NOT recommend actions
""",
        model=model
    )

portfolio_agent = create_market_agent()