import sqlalchemy as sa

from database.engine import AsyncSession
from database.models import TaskModel


class TaskRepo:
    """Класс отвечающий за действия с задачами. На уровне БД"""

    @staticmethod
    async def insert(
        session: AsyncSession,
        user_id: int,
        name: str,
        description: str,
    ) -> None:
        """Добавление задачи."""
        query = (
            sa.insert(TaskModel)
            .values(
                user_id=user_id,
                name=name,
                description=description,
            )
            .returning(TaskModel.id)
        )
        user_id = await session.scalar(query)
        return user_id

    @staticmethod
    async def select_by_id_and_user_id(
        session: AsyncSession,
        user_id: int,
    ) -> tuple:
        """Получение всех задач пользователя."""
        query = (
            sa.select(
                TaskModel.id,
                TaskModel.name,
                TaskModel.description,
                TaskModel.state,
            )
            .where(TaskModel.user_id == user_id)
            .order_by(TaskModel.id)
        )
        res = await session.execute(query)
        return res.all()

    @staticmethod
    async def update(
        session: AsyncSession,
        task_id: int,
        **kwargs,
    ) -> None:
        """Обновление задачи."""
        query = sa.update(TaskModel).where(TaskModel.id == task_id).values(**kwargs)
        await session.execute(query)

    @staticmethod
    async def delete(
        session: AsyncSession,
        task_id: int,
    ) -> None:
        """Удаление задачи."""
        query = sa.delete(TaskModel).where(TaskModel.id == task_id)
        await session.execute(query)
