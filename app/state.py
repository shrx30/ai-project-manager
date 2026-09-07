from typing import TypedDict


class ProjectState(TypedDict):
    repository: str
    issues: list
    analysis: str