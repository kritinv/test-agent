from pathlib import Path
import sys

# Keep this file at the repo root, keep the function named `run(input)`,
# and always return the app output as a string.
_AGENT_DIR = Path(__file__).resolve().parent / "agents" / "01-web-research-agent"
sys.path.insert(0, str(_AGENT_DIR))

from agent import build_graph  # noqa: E402


def run(input):
    if isinstance(input, dict):
        query = input.get("query", input.get("input", str(input)))
    else:
        query = input if isinstance(input, str) else str(input)
    agent = build_graph()
    result = agent.invoke({"query": query, "messages": [], "search_results": [], "report": ""})
    return str(result.get("report", ""))
