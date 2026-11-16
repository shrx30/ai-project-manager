from app.actions.models import ProposedAction


class ActionStore:
    """In-memory storage for proposed actions."""

    def __init__(self):
        self._actions: dict[str, ProposedAction] = {}

    def save(self, action: ProposedAction) -> ProposedAction:
        """Save or update an action."""

        self._actions[action.action_id] = action

        return action

    def get(self, action_id: str) -> ProposedAction | None:
        """Retrieve an action by its ID."""

        return self._actions.get(action_id)

    def delete(self, action_id: str) -> bool:
        """Delete an action by its ID."""

        if action_id not in self._actions:
            return False

        del self._actions[action_id]

        return True

    def list_all(self) -> list[ProposedAction]:
        """Return all stored actions."""

        return list(self._actions.values())


action_store = ActionStore()