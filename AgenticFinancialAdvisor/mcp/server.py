import json
from pathlib import Path
from fastmcp import FastMCP

DATA_DIR = Path(__file__).parent.parent / "data"

mcp = FastMCP("advisor-data-server")

@mcp.tool()
def get_client_profile() -> dict:
    with open(DATA_DIR / "client_profile.json") as f:
        return json.load(f)

@mcp.tool()
def get_portfolio() -> dict:
    with open(DATA_DIR / "portfolio.json") as f:
        return json.load(f)

@mcp.tool()
def get_market_news() -> list:
    with open(DATA_DIR / "market_news.json") as f:
        return json.load(f)

if __name__ == "__main__":
    # 🚨 REQUIRED when using MCPServerStdio
    mcp.run()