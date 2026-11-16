from app.actions.approval import approve_action
from app.actions.executor import execute_action
from app.actions.models import (
    ActionResult,
    ApprovalStatus,
    ProposedAction,
)


def approve_and_execute_action(
    action: ProposedAction,
    dry_run: bool = True,
) -> ActionResult:
    """
    Approve and execute a proposed action.

    Args:
        action: The proposed action.
        dry_run: If True, do not modify GitHub.

    Returns:
        ActionResult containing the execution outcome.
    """

    # 1. Approve the action
    approval_result = approve_action(action)

    if not approval_result.success:
        return approval_result

    # 2. Execute the approved action
    execution_result = execute_action(
        action=action,
        dry_run=dry_run,
    )

    # 3. Update status only for real execution
    if not dry_run:
        if execution_result.success:
            action.approval_status = ApprovalStatus.EXECUTED
        else:
            action.approval_status = ApprovalStatus.FAILED

    return execution_result