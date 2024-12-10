import asyncio

from pyrogram.types import Message, ReplyKeyboardMarkup

from common.enum import ButtonStates, Callback, FsmStates, TextAnswer, TextConstants
from common.fsm import fsm
from database.engine import AsyncSession
from repositories.task import TaskRepo
from services.buttons import buttons
from services.inlines import inlines
from services.mixins.protocol import TypeProtocol


class TaskHandlerMixin:
    """Класс отвечающий за действия с задачами."""

    task_repo = TaskRepo

    def __init__(self: TypeProtocol):
        """Регестрируем действия с задачами."""
        super().__init__()
        self.option_map.update(
            {
                FsmStates.add_task: self.add_task,
                FsmStates.show_tasks: self.show_tasks,
                FsmStates.add_name_task: self.add_name_task,
                FsmStates.add_description_task: self.add_description_task,
                FsmStates.done_task: self.done_task,
                FsmStates.delete_task: self.delete_task,
            }
        )

        self.state_map.update(
            {
                ButtonStates.add_task: FsmStates.add_task,
                ButtonStates.show_tasks: FsmStates.show_tasks,
                Callback.done: FsmStates.done_task,
                Callback.delete: FsmStates.delete_task,
            }
        )

    @staticmethod
    async def show_tasks(message: Message, user_id: int, **kwargs) -> None | tuple[str, None]:
        """Показать задачи пользователя."""
        async with AsyncSession() as session:
            tasks = await TaskRepo.select_by_id_and_user_id(
                session=session,
                user_id=user_id,
            )

        if not tasks:
            return TextConstants.tasks_not_found, buttons.menu_buttons()

        back_tasks = [
            message.reply(
                TextAnswer.show_tasks.formatting_value(
                    task.name,
                    task.description,
                    TextConstants.completed if task.state else TextConstants.not_completed,
                ),
                reply_markup=inlines.show_tasks(
                    task_id=task.id,
                    state=task.state,
                ),
            )
            for task in tasks
        ]
        await asyncio.gather(*back_tasks)

    @classmethod
    async def done_task(cls, task_id: int) -> tuple[str, ReplyKeyboardMarkup]:
        """Завершить задачу."""
        async with AsyncSession() as session:
            await cls.task_repo.update(session=session, task_id=task_id, state=True)
            await session.commit()
        return TextConstants.task_completed, buttons.menu_buttons()

    @classmethod
    async def delete_task(cls, task_id: int) -> tuple[str, ReplyKeyboardMarkup]:
        """Удалить задачу."""
        async with AsyncSession() as session:
            await cls.task_repo.delete(session=session, task_id=task_id)
            await session.commit()
        return TextConstants.task_deleted, buttons.menu_buttons()

    @staticmethod
    async def add_task(user_id: int, **kwargs) -> tuple[str, None]:
        """Добавить задачу."""
        fsm.set_state(user_id, FsmStates.add_name_task)
        return TextConstants.input_name_task, None

    @staticmethod
    async def add_name_task(text: str, user_id: int, **kwargs) -> tuple[str, None]:
        """Добавить название задачи."""
        fsm.set_data(user_id, 'task_name', text)
        fsm.set_state(user_id, FsmStates.add_description_task)
        return TextConstants.input_description_task, None

    @classmethod
    async def add_description_task(cls, text: str, user_id: int, **kwargs) -> tuple[str, None]:
        """Добавить описание задачи и сохранить."""
        task_name = fsm.get_data(user_id, 'task_name')
        task_description = text

        async with AsyncSession() as session:
            await cls.task_repo.insert(
                session=session,
                user_id=user_id,
                name=task_name,
                description=task_description,
            )
            await session.commit()
        fsm.reset(user_id)
        return TextAnswer.task_added.formatting_value(task_name), buttons.menu_buttons()
