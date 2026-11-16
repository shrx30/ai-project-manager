
from datetime import datetime

from pydantic import BaseModel


class GitHubIssue(BaseModel):
    number: int
    title: str
    body: str | None = None

    created_at: datetime
    updated_at: datetime

    labels: list[str] = []
    assignee: str | None = None
