from github import Github
from app.models.issue import GitHubIssue


class GitHubService:
    def __init__(self, github_client: Github):
        self.github = github_client

    def list_issues(self, owner: str, repo_name: str):
        repo = self.github.get_repo(f"{owner}/{repo_name}")
        issues = repo.get_issues(state="open")

        return [
            GitHubIssue(
                number=issue.number,
                title=issue.title,
                body=issue.body,
                created_at=issue.created_at,
                updated_at=issue.updated_at,
                labels=[label.name for label in issue.labels],
                assignee=issue.assignee.login if issue.assignee else None,
            )
            for issue in issues
            if not issue.pull_request
        ]

    def get_pull_requests(self, owner: str, repo_name: str, pr_numbers: list[int]):
        repo = self.github.get_repo(f"{owner}/{repo_name}")
        pull_requests = []

        for number in pr_numbers:
            pr = repo.get_pull(number)
            pull_requests.append({
                "number": pr.number,
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "merged": pr.merged,
                "draft": pr.draft,
                "author": pr.user.login if pr.user else None,
            })

        return pull_requests
