import os

from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

llm = ChatNVIDIA(
    model="moonshotai/kimi-k3",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0,
    max_completion_tokens=2048,
    timeout=180,
)


def analyze_issues(issues: list) -> str:

    prompt = f"""
You are an AI project manager.

Analyze the following GitHub issues.

Identify issues that appear:
1. stale
2. blocked
3. waiting on another person
4. at risk of becoming delayed

For every suspicious issue:
- give the issue number
- explain the evidence
- identify the likely blocker
- recommend what a project manager should investigate next

Do not invent information.
Only use evidence contained in the issue data.

GitHub issues:

{issues}
"""

    response = llm.invoke(prompt)

    return response.content