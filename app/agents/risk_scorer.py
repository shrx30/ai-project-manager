
from datetime import datetime, timezone




def calculate_risk(issue: dict) -> dict:
    score = 0
    reasons = []

    updated_at = datetime.fromisoformat(
        issue["updated_at"].replace("Z", "+00:00")
    )

    days_inactive = (
        datetime.now(timezone.utc) - updated_at
    ).days

    if days_inactive >= 60:
        score += 35
        reasons.append("Inactive for 60+ days")
    elif days_inactive >= 30:
        score += 20
        reasons.append("Inactive for 30+ days")

    if not issue.get("assignee"):
        score += 10
        reasons.append("No assignee")

    labels = [
        label.lower() for label in issue.get("labels", [])
    ]

    if "blocked" in labels:
        score += 30
        reasons.append("Blocked label")

    if "bug" in labels or "critical" in labels:
        score += 20
        reasons.append("Bug or critical label")

    score = min(score, 100)

    if score >= 60:
        level = "high"
    elif score >= 30:
        level = "medium"
    else:
        level = "low"

    return {
        "issue_number": issue["number"],
        "risk_score": score,
        "risk_level": level,
        "days_inactive": days_inactive,
        "reasons": reasons,
    }

