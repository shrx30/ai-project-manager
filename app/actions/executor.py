
from app.actions.models import (
    ActionResult,
    ActionType,
    ApprovalStatus,
    ProposedAction,
)
from app.tools.github import get_github_repo


def execute_action(
    action: ProposedAction,
    dry_run: bool = True,
) -> ActionResult:
    """
    Execute an approved GitHub action.

    Args:
        action: The proposed action.
        dry_run: If True, do not modify GitHub.

    Currently supported:
        - ADD_LABEL
    """

    # 1. Verify approval
    if action.approval_status != ApprovalStatus.APPROVED:
        return ActionResult(
            action_id=action.action_id,
            success=False,
            message=(
                "Action cannot be executed. "
                f"Current status: {action.approval_status.value}"
            ),
        )

    # 2. Verify supported action type
    if action.action_type != ActionType.ADD_LABEL:
        return ActionResult(
            action_id=action.action_id,
            success=False,
            message=(
                f"Action type '{action.action_type.value}' "
                "is not implemented yet."
            ),
        )

    # 3. Validate payload
    issue_number = action.payload.issue_number
    label = action.payload.label

    if issue_number is None:
        return ActionResult(
            action_id=action.action_id,
            success=False,
            message="Missing issue_number in action payload.",
        )

    if not label or not label.strip():
        return ActionResult(
            action_id=action.action_id,
            success=False,
            message="Missing label in action payload.",
        )

    label = label.strip()

    # 4. Dry-run mode
    if dry_run:
        return ActionResult(
            action_id=action.action_id,
            success=True,
            message=(
                "Dry run successful. "
                f"Label '{label}' would be added "
                f"to issue #{issue_number}."
            ),
            data={
                "dry_run": True,
                "issue_number": issue_number,
                "label": label,
            },
        )

    # 5. Execute real GitHub action
    try:
        repo = get_github_repo()

        issue = repo.get_issue(number=issue_number)

        issue.add_to_labels(label)

        return ActionResult(
            action_id=action.action_id,
            success=True,
            message=(
                f"Label '{label}' added "
                f"to issue #{issue_number}."
            ),
            data={
                "dry_run": False,
                "issue_number": issue_number,
                "label": label,
            },
        )

    except Exception as error:
        return ActionResult(
            action_id=action.action_id,
            success=False,
            message=f"GitHub action failed: {str(error)}",
        )