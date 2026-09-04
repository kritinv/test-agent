"""Confident eval entrypoint.

Keep this file at the repo root with a single `run(input)` function that returns
the app output as a string
"""

from importlib.util import module_from_spec, spec_from_file_location
from json import loads
from pathlib import Path

_AGENT_PATH = Path(__file__).resolve().parent / "agents" / "01-web-research-agent" / "agent.py"
_AGENT_MODULE = None
_GRAPH = None


def _load_agent_module():
    spec = spec_from_file_location("web_research_agent", _AGENT_PATH)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run(input):
    """Run the app on one input and return a string result."""
    global _AGENT_MODULE, _GRAPH

    if _AGENT_MODULE is None:
        _AGENT_MODULE = _load_agent_module()
    if _GRAPH is None:
        _GRAPH = _AGENT_MODULE.build_graph()

    query = input
    if isinstance(input, dict):
        query = input.get("query", input)
    elif isinstance(input, str):
        text = input.strip()
        if text.startswith("{"):
            try:
                parsed = loads(text)
            except Exception:
                parsed = None
            if isinstance(parsed, dict):
                query = parsed.get("query", input)

    result = _GRAPH.invoke({"query": str(query), "messages": [], "search_results": [], "report": ""})
    return str(result.get("report", ""))
