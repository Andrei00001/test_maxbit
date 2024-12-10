from typing import Any, Dict


class FSMContext:
    """Класс для хранения состояний пользователей."""

    def __init__(self):
        self.states: Dict[int, Dict[str, Any]] = {}

    def set_state(self, user_id: int, state: str) -> None:
        """Установка состояния пользователя."""
        if user_id not in self.states:
            self.states[user_id] = {}
        self.states[user_id]['state'] = state

    def get_state(self, user_id: int) -> str | None:
        """Получение состояния пользователя."""
        return self.states.get(user_id, {}).get('state', None)

    def set_data(self, user_id: int, key: str, value: Any):
        """Сохранение данных пользователя."""
        if user_id not in self.states:
            self.states[user_id] = {}
        self.states[user_id][key] = value

    def get_data(self, user_id: int, key: str) -> Any:
        """Получение данных пользователя."""
        return self.states.get(user_id, {}).get(key, None)

    def reset(self, user_id: int):
        """Сброс состояния пользователя."""
        if user_id in self.states:
            del self.states[user_id]


fsm = FSMContext()
