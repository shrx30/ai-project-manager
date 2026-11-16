from app.actions.approval import (
    approve_action,
    reject_action,
)
from app.actions.models import (
    ActionPayload,
    ActionType,
    ApprovalStatus,
    ProposedAction,
)
from app.actions.service import (
    approve_and_execute_action,
)


def create_test_action() -> ProposedAction:
    """Create a reusable test action."""

    return ProposedAction(
        action_type=ActionType.ADD_LABEL,
        payload=ActionPayload(
            issue_number=10370,
            label="ai-test-label",
        ),
        reason="Automated test action",
    )


def test_approve_pending_action():
    """A pending action should be approved successfully."""

    action = create_test_action()

    result = approve_action(action)

    assert result.success is True
    assert action.approval_status == ApprovalStatus.APPROVED


def test_reject_pending_action():
    """A pending action should be rejected successfully."""

    action = create_test_action()

    result = reject_action(action)

    assert result.success is True
    assert action.approval_status == ApprovalStatus.REJECTED


def test_rejected_action_cannot_be_approved():
    """A rejected action cannot be approved again."""

    action = create_test_action()

    reject_action(action)
    result = approve_action(action)

    assert result.success is False
    assert action.approval_status == ApprovalStatus.REJECTED


def test_dry_run_execution():
    """An approved action should execute successfully in dry-run mode."""

    action = create_test_action()

    result = approve_and_execute_action(
        action=action,
        dry_run=True,
    )

    assert result.success is True
    assert result.data["dry_run"] is True
    assert action.approval_status == ApprovalStatus.APPROVED