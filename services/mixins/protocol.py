from typing import Callable, Protocol

from pyrogram.types import Message, ReplyKeyboardMarkup


class TypeProtocol(Protocol):
    """Протакол для классов."""

    option_map: dict[str, Callable]
    state_map: dict[str, str]

    @staticmethod
    async def add_task(user_id: int, **kwargs) -> tuple[str, None]: ...

    @staticmethod
    async def show_tasks(message: Message, user_id: int, **kwargs) -> None | tuple[str, None]: ...

    @classmethod
    async def done_task(cls, task_id: int) -> tuple[str, ReplyKeyboardMarkup]: ...

    @classmethod
    async def add_description_task(cls, text: str, user_id: int, **kwargs) -> tuple[str, None]: ...

    @staticmethod
    async def add_name_task(text: str, user_id: int, **kwargs) -> tuple[str, None]: ...

    @classmethod
    async def delete_task(cls, task_id: int) -> tuple[str, ReplyKeyboardMarkup]: ...

    @staticmethod
    async def register_username(text: str, user_id: int, **kwargs) -> tuple[str, None]: ...

    @classmethod
    async def register_login(
        cls,
        text: str,
        user_id: int,
        **kwargs,
    ) -> tuple[str, ReplyKeyboardMarkup]: ...
