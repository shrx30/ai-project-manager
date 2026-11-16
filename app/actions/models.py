
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """Supported GitHub actions."""

    CREATE_ISSUE = "create_issue"
    ADD_COMMENT = "add_comment"
    ADD_LABEL = "add_label"
    ASSIGN_ISSUE = "assign_issue"
    CLOSE_ISSUE = "close_issue"


class ApprovalStatus(str, Enum):
    """Approval lifecycle for an action."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"


class ActionPayload(BaseModel):
    """Data required to execute a GitHub action."""

    issue_number: int | None = None
    title: str | None = None
    body: str | None = None
    label: str | None = None
    assignee: str | None = None


class ProposedAction(BaseModel):
    """An action proposed by the AI and awaiting approval."""

    action_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    action_type: ActionType

    payload: ActionPayload

    reason: str = Field(
        min_length=1,
        description="Why the AI proposed this action.",
    )

    approval_status: ApprovalStatus = (
        ApprovalStatus.PENDING
    )


class ActionResult(BaseModel):
    """Result returned after attempting an action."""

    action_id: str

    success: bool

    message: str

    data: dict[str, Any] | None = None