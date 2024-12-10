import sqlalchemy as sa
from sqlalchemy import Row

from database.engine import AsyncSession
from database.models import UserModel


class UserRepo:
    """Класс отвечающий за действия с пользователями. На уровне БД"""

    @staticmethod
    async def insert(
        session: AsyncSession,
        user_id: int,
        name: str,
        login: str,
    ) -> None:
        """Добавление пользователя."""
        query = (
            sa.insert(UserModel)
            .values(
                id=user_id,
                name=name,
                login=login,
            )
            .returning(UserModel.id)
        )
        user_id = await session.scalar(query)
        return user_id

    @staticmethod
    async def select_by_id(
        session: AsyncSession,
        user_id: int,
    ) -> Row | None:
        """Получение пользователя по id."""
        query = sa.select(UserModel.name).where(UserModel.id == user_id)
        user = await session.execute(query)
        return user.first()

    @staticmethod
    async def select_by_login(
        session: AsyncSession,
        login: str,
    ) -> Row | None:
        """Получение пользователя по логину."""
        query = sa.select(UserModel.login).where(UserModel.login == login)
        user = await session.execute(query)
        return user.first()
