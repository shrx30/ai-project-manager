
from langgraph.graph import StateGraph, START, END
from app.agents.risk_scorer import calculate_risk

from app.state import ProjectState
from app.agents.investigator import (
    find_candidates,
    find_related_prs,
    analyze_issue_with_pr,
)
from app.agents.risk_scorer import calculate_risk

def score_risks(state: ProjectState):
    investigations = state.get("investigations", [])

    risk_scores = [
        calculate_risk(issue)
        for issue in investigations
    ]

    print("\n===== RISK SCORES =====")

    for risk in risk_scores:
        print(risk)

    return {
        "risk_scores": risk_scores
    }


def create_graph(github_service):

    def get_issues(state: ProjectState):
        owner, repo_name = state["repository"].split("/", 1)

        issues = github_service.list_issues(
            owner=owner,
            repo_name=repo_name,
        )

        # Convert Pydantic objects into dictionaries
        return {
            "issues": [
                issue.model_dump(mode="json")
                for issue in issues
            ]
        }

    def select_candidates(state: ProjectState):
        candidates = find_candidates(state["issues"])

        return {"candidate_numbers": candidates}

    def investigate(state: ProjectState):
        candidate_numbers = set(state["candidate_numbers"])

        selected_issues = [
            issue
            for issue in state["issues"]
            if issue["number"] in candidate_numbers
        ]

        return {"investigations": selected_issues}

    def find_prs(state: ProjectState):
        prs = find_related_prs(state["investigations"])

        return {"related_pr_numbers": prs}

    def final_analysis(state: ProjectState):
        results = analyze_issue_with_pr(
            state["investigations"],
            state.get("pull_requests", []),
        )

        return {"analysis": results}

    def fetch_pull_requests(state: ProjectState):
     owner, repo_name = state["repository"].split("/", 1)

     pull_requests = github_service.get_pull_requests(
        owner=owner,
        repo_name=repo_name,
        pr_numbers=state["related_pr_numbers"],
     )

     return {"pull_requests": pull_requests}

    builder = StateGraph(ProjectState)

    builder.add_node("get_issues", get_issues)
    builder.add_node("select_candidates", select_candidates)
    builder.add_node("investigate", investigate)
    builder.add_node("find_prs", find_prs)
    builder.add_node("final_analysis", final_analysis)
    builder.add_node("fetch_pull_requests", fetch_pull_requests)
    builder.add_node("score_risks", score_risks)

    builder.add_edge("find_prs", "fetch_pull_requests")
    builder.add_edge("fetch_pull_requests", "final_analysis")

    builder.add_edge(START, "get_issues")
    builder.add_edge("get_issues", "select_candidates")
    builder.add_edge("select_candidates", "investigate")
    
    builder.add_edge("investigate", "score_risks")
    builder.add_edge("score_risks", "find_prs")
    builder.add_edge("final_analysis", END)

    return builder.compile()
