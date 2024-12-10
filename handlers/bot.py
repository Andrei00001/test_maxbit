from typing import Callable, Type

from common.enum import FsmStates, TextAnswer, TextConstants
from common.fsm import fsm
from database.engine import AsyncSession
from repositories.user import UserRepo
from services.mixins.task import TaskHandlerMixin
from services.mixins.user import UserHandlerMixin


class BotHandler(UserHandlerMixin, TaskHandlerMixin):
    """
    Маршрутизатор по желаемым дейсткиям пользователя
    + стартовые функцие отвечающие за старт бота и сообщения не относящиеся к действиям
    """

    user_repo = UserRepo
    option_map = {}
    state_map = {}

    def filter_state(
        self,
        user_id: int,
        option: str | None,
    ) -> Type[Callable] | None:
        """Функиця маршрутизатор по действия"""

        option = fsm.get_state(user_id) or self.state_map.get(option, option)

        if not option:
            return None

        return self.option_map[option]

    @classmethod
    async def start(cls, *, user_id: int) -> tuple[str, None]:
        """Функционал отвещающий за команду /start"""

        async with AsyncSession() as session:
            user = await cls.user_repo.select_by_id(session=session, user_id=user_id)

        if user:
            return TextAnswer.welcome_text.formatting_value(user.name), None

        state = fsm.get_state(user_id)
        if state:
            return TextConstants.in_state_register, None
        else:
            fsm.set_state(user_id, FsmStates.register_username)
            return TextConstants.welcome_text, None

    @staticmethod
    async def handle_text() -> tuple[str, None]:
        """Ответ на любое сообщение не относящаеся к действию"""
        return TextConstants.some_text, None
