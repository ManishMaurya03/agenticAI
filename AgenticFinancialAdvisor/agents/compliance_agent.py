from agents import Agent
from langfuse.openai import OpenAI
from langfuse import observe
from config import OPENAI_API_KEY, MODEL_CHOICE

client = OpenAI(api_key=OPENAI_API_KEY)
model = MODEL_CHOICE

@observe(name="ComplianceGuardAgent")
def create_compliance_agent():
    return Agent(
        name="ComplianceGuardAgent",
        instructions="""
You are a compliance guard for a US financial services firm.

Responsibilities:
- Detect risky or advisory language
- Rewrite in compliant, neutral form
- Add disclosures if needed
""",
        model=model
    )

compliance_agent = create_compliance_agent()