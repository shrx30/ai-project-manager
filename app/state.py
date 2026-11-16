
from typing import TypedDict, Any


class ProjectState(TypedDict):
    repository: str
    issues: list[dict]
    candidate_numbers: list[int]
    investigations: list[dict]
    related_pr_numbers: list[int]
    pull_requests: list[dict]
    analysis: Any
    risk_scores: list[dict]
