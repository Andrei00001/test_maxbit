from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from common.enum import Callback, TextConstants


class Inlines:
    """Класс для создания inline кнопок."""

    @classmethod
    def show_tasks(
        cls,
        state: bool,
        task_id: int = 0,
    ):
        """Кнопки для задач."""
        group_1 = []
        if not state:
            group_1.append(Inlines._done_task(task_id))
        group_1.append(Inlines._delete_task(task_id))
        return cls.__build(group_1)

    @staticmethod
    def _done_task(
        task_id: int,
    ):
        """Кнопка завершения задачи."""
        return InlineKeyboardButton(
            TextConstants.execute, callback_data=f"{task_id}_{Callback.done}"
        )

    @staticmethod
    def _delete_task(
        task_id: int,
    ):
        """Кнопка удаления задачи."""
        return InlineKeyboardButton(
            TextConstants.delete, callback_data=f"{task_id}_{Callback.delete}"
        )

    @classmethod
    def __build(cls, *args):
        """Создание клавиатуры."""
        return InlineKeyboardMarkup([*args])


inlines = Inlines()
