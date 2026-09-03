from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any


# Keep this file at the repo root.
# Keep the function named run(input) and return the app output as a string.
_AGENT_GRAPH = None


def _load_agent_graph():
    global _AGENT_GRAPH
    if _AGENT_GRAPH is not None:
        return _AGENT_GRAPH

    agent_path = Path(__file__).parent / "agents" / "01-web-research-agent" / "agent.py"
    spec = spec_from_file_location("web_research_agent", agent_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load agent module from {agent_path}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    _AGENT_GRAPH = module.build_graph()
    return _AGENT_GRAPH


def run(input: Any) -> str:
    if isinstance(input, dict):
        query = input.get("query", input.get("input", ""))
    else:
        query = input
    query = str(query)

    result = _load_agent_graph().invoke(
        {"query": query, "messages": [], "search_results": [], "report": ""}
    )
    report = result.get("report", "")
    return report if isinstance(report, str) else str(report)
