from fastapi import APIRouter, HTTPException
from app.actions.proposer import (
    propose_investigation_label,
)

from app.actions.models import (
    ActionPayload,
    ActionType,
    ProposedAction,
ApprovalStatus
)
from app.actions.service import (
    approve_and_execute_action,
)
from app.actions.approval import approve_action
from app.actions.store import action_store
from app.actions.executor import execute_action
from app.actions.models import ApprovalStatus

router = APIRouter(
    prefix="/actions",
    tags=["Actions"],
)


@router.post("/dry-run")
def dry_run_action(
    action_type: ActionType,
    payload: ActionPayload,
    reason: str,
):
    """
    Approve and execute an action in dry-run mode.
    """

    action = ProposedAction(
        action_type=action_type,
        payload=payload,
        reason=reason,
    )

    result = approve_and_execute_action(
        action=action,
        dry_run=True,
    )

    if not result.success:
        raise HTTPException(
            status_code=400,
            detail=result.message,
        )

    return {
        "action": action.model_dump(),
        "result": result.model_dump(),
    }
@router.post("/propose-label")
def propose_label_action(
    issue_number: int,
    reason: str,
    label: str = "investigate",
):
    """
    Create a proposed label action for a GitHub issue.

    The action remains pending until approved.
    """

    try:
        action = propose_investigation_label(
            issue_number=issue_number,
            reason=reason,
            label=label,
        )
        action_store.save(action)

        return {
            "action": action.model_dump(),
            "message": (
                "Action proposed successfully. "
                "Human approval is required."
            ),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
@router.post("/{action_id}/approve")
def approve_stored_action(action_id: str):
    action = action_store.get(action_id)

    if action is None:
        raise HTTPException(
            status_code=404,
            detail="Action not found.",
        )

    result = approve_action(action)

    if not result.success:
        raise HTTPException(
            status_code=400,
            detail=result.message,
        )

    return {
        "action": action.model_dump(),
        "result": result.model_dump(),
    }
@router.post("/{action_id}/execute")
def execute_stored_action(
    action_id: str,
    confirm: bool = False,
):
    """
    Execute an approved action against GitHub.

    Real execution requires explicit confirmation.
    """

    action = action_store.get(action_id)

    if action is None:
        raise HTTPException(
            status_code=404,
            detail="Action not found.",
        )

    if action.approval_status != ApprovalStatus.APPROVED:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only approved actions can be executed. "
                f"Current status: {action.approval_status.value}"
            ),
        )

    if not confirm:
        raise HTTPException(
            status_code=400,
            detail=(
                "Real execution requires explicit confirmation. "
                "Set confirm=true."
            ),
        )

    result = execute_action(
        action=action,
        dry_run=False,
    )

    if result.success:
        action.approval_status = ApprovalStatus.EXECUTED
    else:
        action.approval_status = ApprovalStatus.FAILED

    return {
        "action": action.model_dump(),
        "result": result.model_dump(),
        "message": "Action executed against GitHub.",
    }