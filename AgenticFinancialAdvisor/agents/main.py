import asyncio
from langfuse import observe
from agents.mcp import MCPServerStdio
from orchestrator import run_orchestrator
import json

import json

def extract_json(tool_result):
    """
    Extract JSON payload from MCP CallToolResult safely.
    Works with MCP versions using camelCase fields.
    """

    # MCP error handling
    if getattr(tool_result, "isError", False):
        raise RuntimeError(f"MCP tool error: {tool_result}")

    if not tool_result.content:
        raise RuntimeError("MCP tool returned empty content")

    return json.loads(tool_result.content[0].text)

@observe(name="advisor-briefing-session")
async def main():

    # Start MCP server via stdio
    async with MCPServerStdio(
        name="advisor_data_mcp",
        params={
            "command": "python3",
            "args": ["/Users/manishmaurya/Desktop/OpenAIApplications/AgenticFinancialAdvisor/mcp/server.py"]
        }
    ) as mcp:

        # ✅ CRITICAL FIX: unwrap MCP results
        client_profile = extract_json(
            await mcp.call_tool("get_client_profile", {})
        )

        portfolio = extract_json(
            await mcp.call_tool("get_portfolio", {})
        )

        market_news = extract_json(
            await mcp.call_tool("get_market_news", {})
        )

        result = await run_orchestrator(
            client_profile=client_profile,
            portfolio=portfolio,
            market_news=market_news
        )

        print("\n===== ADVISOR MEETING BRIEF =====\n")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
    