from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup

from common.enum import ButtonStates


class Buttons:
    """Класс для создания кнопок."""

    @classmethod
    def menu_buttons(cls):
        """Кнопки главного меню для создания задач."""
        return cls.__build(
            [cls._add_task()],
            [cls._show_tasks()],
        )

    @staticmethod
    def _add_task():
        """Кнопка добавления задачи."""
        return KeyboardButton(ButtonStates.add_task)

    @staticmethod
    def _show_tasks():
        """Кнопка просмотра задач."""
        return KeyboardButton(ButtonStates.show_tasks)

    @staticmethod
    def __build(*args):
        """Создание клавиатуры."""
        return ReplyKeyboardMarkup([*args], resize_keyboard=True)


buttons = Buttons()
