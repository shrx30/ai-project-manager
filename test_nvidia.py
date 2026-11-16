
import os

from dotenv import load_dotenv
from github import Github, Auth

from app.tools.github import GitHubService

load_dotenv(override=True)

token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN not found in .env")

print("GitHub token loaded:", bool(token))

# Create authenticated client
auth = Auth.Token(token)
client = Github(auth=auth)

try:
    github_service = GitHubService(client)

    issues = github_service.list_issues(
        owner=os.getenv("GITHUB_REPO_OWNER"),
        repo_name=os.getenv("GITHUB_REPO_NAME"),
    )

    print(f"Fetched {len(issues)} issues")

    for issue in issues:
        print(f"#{issue.number}: {issue.title}")

finally:
    client.close()
