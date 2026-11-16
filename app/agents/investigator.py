import json
import os

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

llm = ChatNVIDIA(
    model=os.getenv("NVIDIA_MODEL", "meta/muse-glimmer-30b"),
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0,
    max_completion_tokens=2048,
    timeout=180,
)


class CandidateIssues(BaseModel):
    issue_numbers: list[int]


class RelatedPRs(BaseModel):
    pr_numbers: list[int]


class InvestigationResult(BaseModel):
    issue_number: int
    status: str
    evidence: str
    blocker: str
    next_action: str



def find_candidates(issues: list) -> list[int]:
    if not issues:
        print("No GitHub issues received.")
        return []

    print("\n===== ISSUES RECEIVED BY CANDIDATE SELECTOR =====")
    print(json.dumps(issues, indent=2, default=str))

    prompt = f"""
You are an AI project manager.

Identify up to 5 GitHub issues that may be:
- Stale
- Blocked
- Waiting on another person
- At risk of delay
- Missing clear ownership or next steps

GitHub issues:
{json.dumps(issues, default=str)}

Return ONLY JSON:
{{"issue_numbers": [10370]}}

Do not invent issue numbers.
"""

    response = llm.invoke(prompt)

    print("\n===== RAW CANDIDATE RESPONSE =====")
    print(response.content)

    try:
        data = json.loads(response.content)
        result = CandidateIssues.model_validate(data)

        valid_numbers = {issue["number"] for issue in issues}

        candidates = [
            number for number in result.issue_numbers
            if number in valid_numbers
        ]

    except (json.JSONDecodeError, ValidationError) as error:
        print("Candidate parsing error:", error)
        candidates = []

    # Fallback for pipeline testing
    if not candidates:
        candidates = [issue["number"] for issue in issues[:5]]

    print("\n===== FINAL SELECTED CANDIDATES =====")
    print(candidates)

    return candidates[:5]



def find_related_prs(investigations: list) -> list[int]:

    prompt = f"""
You are an AI project manager.

Review these GitHub issue investigations.

Identify pull requests that are explicitly mentioned in the
issue title, body, or comments and that appear relevant to
the issue's potential blocker or risk.

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "pr_numbers": [5707]
}}

Rules:
- Only return PR numbers explicitly mentioned in the provided data.
- Do not invent PR numbers.
- Return at most 5 PR numbers.

Investigations:

{investigations}
"""

    response = llm.invoke(prompt)

    print("\n===== RAW RELATED PR RESPONSE =====\n")
    print(response.content)

    try:
        data = json.loads(response.content)
        result = RelatedPRs.model_validate(data)

    except (json.JSONDecodeError, ValidationError) as error:
        print("\n===== PR PARSING ERROR =====\n")
        print(error)
        return []

    return result.pr_numbers[:5]


def analyze_issue_with_pr(
    investigations: list,
    pull_requests: list,
) -> list[InvestigationResult]:

    prompt = f"""
You are an AI project manager.

Analyze the GitHub issues together with their related pull requests.

Determine whether each issue appears:

- stale
- blocked
- at risk
- normal

Use the pull request information to improve the investigation.

For each issue, determine:

- issue_number
- status
- evidence
- blocker
- next_action

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "results": [
        {{
            "issue_number": 10370,
            "status": "at_risk",
            "evidence": "The issue references a long-standing pull request that is not merged.",
            "blocker": "Review or maintainer capacity",
            "next_action": "Investigate the PR review history and determine what is preventing completion."
        }}
    ]
}}

Rules:
- issue_number must come from the provided issues.
- Do not invent information.
- Use only evidence contained in the provided issues and pull requests.
- The blocker must be supported by the evidence.
- The next_action should be a concrete project-management investigation.
- Return one result for each investigated issue.

GitHub issue investigations:

{investigations}

Related pull requests:

{pull_requests}
"""

    response = llm.invoke(prompt)

    print("\n===== RAW FINAL ANALYSIS RESPONSE =====\n")
    print(response.content)

    try:
        data = json.loads(response.content)

        results = [
            InvestigationResult.model_validate(item)
            for item in data["results"]
        ]

        return results

    except (json.JSONDecodeError, ValidationError, KeyError) as error:
        print("\n===== FINAL ANALYSIS PARSING ERROR =====\n")
        print(error)
        return []







