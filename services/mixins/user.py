from pyrogram.types import ReplyKeyboardMarkup

from common.enum import FsmStates, TextAnswer, TextConstants
from common.fsm import fsm
from database.engine import AsyncSession
from repositories.user import UserRepo
from services.buttons import buttons
from services.mixins.protocol import TypeProtocol


class UserHandlerMixin:
    """Класс отвечающий за действия с пользователем."""

    user_repo = UserRepo

    def __init__(self: TypeProtocol):
        """Регестрируем действия с пользователем."""
        super().__init__()
        self.option_map.update(
            {
                FsmStates.register_username: self.register_username,
                FsmStates.register_login: self.register_login,
            }
        )

    @staticmethod
    async def register_username(text: str, user_id: int, **kwargs) -> tuple[str, None]:
        """Запоминание имени пользователя."""
        fsm.set_data(user_id, 'name', text)
        fsm.set_state(user_id, FsmStates.register_login)
        return TextConstants.input_uniq_login, None

    @classmethod
    async def register_login(
        cls,
        text: str,
        user_id: int,
        **kwargs,
    ) -> tuple[str, ReplyKeyboardMarkup | None]:
        """Регистрация пользователя с проверкай на уникальный логин."""
        async with AsyncSession() as session:
            user = await cls.user_repo.select_by_login(session=session, login=text)

        if user:
            return TextConstants.login_exists, None

        name = fsm.get_data(user_id, 'name')
        async with AsyncSession() as session:
            await cls.user_repo.insert(
                session=session,
                user_id=user_id,
                name=name,
                login=text,
            )
            await session.commit()

        fsm.reset(user_id)
        return TextAnswer.register_completed.formatting_value(name), buttons.menu_buttons()
