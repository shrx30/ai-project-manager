import os

from dotenv import load_dotenv
from github import Github, Auth

from app.tools.github import GitHubService
from app.graph import create_graph

from datetime import datetime, timezone

current_date = datetime.now(timezone.utc).date().isoformat()

load_dotenv()

# Initialize GitHub
client = Github(
    auth=Auth.Token(os.getenv("GITHUB_TOKEN"))
)

try:
    github_service = GitHubService(client)

    # Build graph
    graph = create_graph(github_service)

    # Execute workflow
    result = graph.invoke({
    "repository": "fastapi/fastapi",
    "issues": [],
    "candidate_numbers": [],
    "investigations": [],
    "related_pr_numbers": [],
    "pull_requests": [],
    "analysis": [],
})

    print("\n===== PROJECT ANALYSIS =====\n")
    print(result["analysis"])

finally:
    client.close()