import streamlit as st
import asyncio
import json
import os

from agents.mcp import MCPServerStdio
from orchestrator import run_orchestrator

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Advisor Meeting Prep",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧑‍💼 AI powered Financial Advisor – Client Meeting Prep")
st.caption("AI-powered, compliance-aware briefing for financial advisors")

# ----------------------------
# Helper to extract MCP JSON
# ----------------------------
def extract_json(tool_result):
    if getattr(tool_result, "isError", False):
        raise RuntimeError("MCP tool error")
    return json.loads(tool_result.content[0].text)

# ----------------------------
# Load clients from JSON
# ----------------------------
def load_clients():
    json_path = os.path.join(os.path.dirname(__file__), "../data/client_profile.json")
    with open(json_path, "r") as f:
        clients = json.load(f)
    return clients

def format_client_option(client):
    return f"{client['name']} ({client['client_id']})"

# ----------------------------
# Async runner wrapper
# ----------------------------
async def generate_brief(selected_client):
    async with MCPServerStdio(
        name="advisor_data_mcp",
        params={
            "command": "python3",
            "args": ["/Users/manishmaurya/Desktop/OpenAIApplications/AgenticFinancialAdvisor/mcp/server.py"]
        }
    ) as mcp:

        # Use the selected client profile
        client_profile = selected_client
        
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

        return result, client_profile, portfolio


def run_async(coro):
    return asyncio.run(coro)

# ----------------------------
# Sidebar – Advisor Controls
# ----------------------------
with st.sidebar:
    st.header("Advisor Controls")
    
    # Load all clients
    clients = load_clients()
    client_options = [format_client_option(c) for c in clients]
    
    selected_client_option = st.selectbox(
        "Select Client",
        options=client_options,
        disabled=False
    )
    
    # Get the selected client object
    selected_client = next(c for c in clients if format_client_option(c) == selected_client_option)

    generate = st.button(
        "📄 Prepare Meeting Brief",
        type="primary"
    )

# ----------------------------
# Main Content
# ----------------------------
if generate:
    with st.spinner("Preparing advisor for briefing…"):
        try:
            briefing, client_profile, portfolio = run_async(generate_brief(selected_client))

            st.success("Meeting brief ready")

            # ---- Client Snapshot ----
            st.subheader("👤 Client Snapshot")
            col1, col2, col3 = st.columns(3)
            col1.metric("Client Name", client_profile["name"])
            col2.metric("Age", client_profile["age"])
            col3.metric("Risk Profile", client_profile["risk_tolerance"])

            # ---- Portfolio Overview ----
            st.subheader("📊 Portfolio Overview")
            st.json(portfolio["asset_allocation"])

            # ---- Advisor Brief ----
            st.subheader("📝 Advisor Meeting Brief")
            st.markdown(briefing)

        except Exception as e:
            st.error(f"Failed to generate briefing: {e}")

else:
    st.info(
        " Select Client and Click **Prepare Meeting Brief** to generate a "
        "personalized, compliance-aware client summary."
    )