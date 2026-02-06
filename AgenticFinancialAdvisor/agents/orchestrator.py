import json
from agents import Runner
from client_context_agent import client_context_agent
from portfolio_agent import portfolio_agent
from market_agent import portfolio_agent
from narrative_agent import narrative_agent
from compliance_agent import compliance_agent

async def run_orchestrator(client_profile, portfolio, market_news):

    client_ctx = await Runner.run(
        client_context_agent,
        input=json.dumps(client_profile, indent=2)  # ✅ STRING
    )

    portfolio_ctx = await Runner.run(
        portfolio_agent,
        input=json.dumps(portfolio, indent=2)  # ✅ STRING
    )

    market_ctx = await Runner.run(
        portfolio_agent,
        input=json.dumps(
            {
                "portfolio": portfolio,
                "market_news": market_news
            },
            indent=2
        )
    )

    narrative = await Runner.run(
        narrative_agent,
        input=json.dumps(
            {
                "client": client_ctx.final_output,
                "portfolio": portfolio_ctx.final_output,
                "market": market_ctx.final_output
            },
            indent=2
        )
    )

    compliant = await Runner.run(
        compliance_agent,
        input=narrative.final_output  # already string
    )

    return compliant.final_output