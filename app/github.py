import os

from dotenv import load_dotenv
from github import Github

load_dotenv()

github = Github(os.getenv("GITHUB_TOKEN"))

repo = github.get_repo(
    f"{os.getenv('GITHUB_REPO_OWNER')}/{os.getenv('GITHUB_REPO_NAME')}"
)


def list_issues():
    issues = repo.get_issues(state="open")

    return [
        {
            "number": issue.number,
            "title": issue.title,
            "body": issue.body,
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
            "labels": [label.name for label in issue.labels],
            "assignee": issue.assignee.login if issue.assignee else None,
        }
        for issue in issues
        if not issue.pull_request
    ]