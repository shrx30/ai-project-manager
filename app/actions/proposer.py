from app.actions.models import (
    ActionPayload,
    ActionType,
    ProposedAction,
)


def propose_investigation_label(
    issue_number: int,
    reason: str,
    label: str = "investigate",
) -> ProposedAction:
    """
    Create a proposed action to add a label to a GitHub issue.

    The action is created in PENDING status by default.
    It must be approved before execution.
    """

    if issue_number <= 0:
        raise ValueError(
            "issue_number must be greater than zero."
        )

    if not reason.strip():
        raise ValueError(
            "reason cannot be empty."
        )

    if not label.strip():
        raise ValueError(
            "label cannot be empty."
        )

    return ProposedAction(
        action_type=ActionType.ADD_LABEL,
        payload=ActionPayload(
            issue_number=issue_number,
            label=label.strip(),
        ),
        reason=reason.strip(),
    )