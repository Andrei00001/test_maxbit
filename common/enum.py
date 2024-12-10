from enum import StrEnum


class FsmStates(StrEnum):
    """Состояния конечного автомата."""

    register_username = 'register_username'
    register_login = 'register_login'
    add_task = 'add_task'
    show_tasks = 'show_tasks'
    add_name_task = 'add_name_task'
    add_description_task = 'add_description_task'
    done_task = 'done_task'
    delete_task = 'delete_task'


class ButtonStates(StrEnum):
    """Текст кнопок."""

    add_task = 'Добавить задачу'
    show_tasks = 'Посмотреть задачи'


class TextConstants(StrEnum):
    """Текстовые константы. Для ответов пользователю."""

    execute = 'Выполнить'
    delete = 'Удалить'
    tasks_not_found = 'Задачи отсутствуют'
    completed = 'Выполнена'
    not_completed = 'Не выполнена'
    task_completed = 'Задача выполнена'
    task_deleted = 'Задача удалена'
    input_name_task = 'Введите название задачи:'
    input_description_task = 'Введите описание задачи:'
    input_uniq_login = 'Введите уникальный логин:'
    some_text = 'Привет! Я бот. Напиши /start для регистрации'
    welcome_text = 'Добро пожаловать! Введите ваше имя:'
    in_state_register = 'Вы находитесь в процессе регистрации. Введите ваше имя:'
    login_exists = 'Логин уже существует. Введите другой логин:'


class Callback(StrEnum):
    """Callback data для inline кнопок."""

    done = 'done'
    delete = 'delete'


class TextAnswer(StrEnum):
    """Текстовые ответы для пользователя. С параметрами для форматирования."""

    show_tasks = '**Название**: {}\n**Описание**: {}\n**Статус**: {}\n'
    task_added = 'Задача {} добавлена'
    register_completed = 'Регистрация завершена! Добро пожаловать, {}.'
    welcome_text = 'Добро пожаловать, {}.'

    def formatting_value(self, *args):
        """Форматирование строки."""
        result = self.value
        if args:
            result = self.value.format(*args)
        return result
