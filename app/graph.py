from langgraph.graph import StateGraph, START, END

from app.state import ProjectState
from app.tools.github import list_issues
from app.agents.investigator import analyze_issues


def get_issues(state: ProjectState):
    issues = list_issues()

    return {
        "issues": issues
    }


def investigate(state: ProjectState):
    analysis = analyze_issues(state["issues"])

    return {
        "analysis": analysis
    }


builder = StateGraph(ProjectState)

builder.add_node("get_issues", get_issues)
builder.add_node("investigate", investigate)

builder.add_edge(START, "get_issues")
builder.add_edge("get_issues", "investigate")
builder.add_edge("investigate", END)

graph = builder.compile()