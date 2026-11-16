from app.actions.models import (
    ActionResult,
    ApprovalStatus,
    ProposedAction,
)


def approve_action(action: ProposedAction) -> ActionResult:
    """Approve a pending action without executing it."""

    if action.approval_status != ApprovalStatus.PENDING:
        return ActionResult(
            action_id=action.action_id,
            success=False,
            message=(
                "Only pending actions can be approved. "
                f"Current status: {action.approval_status.value}"
            ),
        )

    action.approval_status = ApprovalStatus.APPROVED

    return ActionResult(
        action_id=action.action_id,
        success=True,
        message="Action approved successfully.",
        data={
            "approval_status": action.approval_status.value,
        },
    )


def reject_action(action: ProposedAction) -> ActionResult:
    """Reject a pending action without executing it."""

    if action.approval_status != ApprovalStatus.PENDING:
        return ActionResult(
            action_id=action.action_id,
            success=False,
            message=(
                "Only pending actions can be rejected. "
                f"Current status: {action.approval_status.value}"
            ),
        )

    action.approval_status = ApprovalStatus.REJECTED

    return ActionResult(
        action_id=action.action_id,
        success=True,
        message="Action rejected successfully.",
        data={
            "approval_status": action.approval_status.value,
        },
    )