from agents import Agent
from langfuse.openai import OpenAI
from langfuse import observe

from config import OPENAI_API_KEY, MODEL_CHOICE

client = OpenAI(api_key=OPENAI_API_KEY)
model = MODEL_CHOICE

@observe(name="NarrativeAgent")
def create_narrative_agent():
    return Agent(
        name="NarrativeAgent",
        instructions="""
You create advisor-ready meeting briefs.

Structure output as:
1. Client Snapshot
2. Portfolio Observations
3. Market Context
4. Discussion Opportunities
5. Key Disclosures

Rules:
- Advisor-friendly language
- No advice or guarantees
""",
        model=model
    )

narrative_agent = create_narrative_agent()