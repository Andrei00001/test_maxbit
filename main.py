from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from common.bot import app
from handlers.bot import BotHandler

bot_handler = BotHandler()


@app.on_message(filters.command('start'))
async def start(_, message: Message) -> None:
    """Handler для команды /start."""
    text, reply_markup = await bot_handler.start(user_id=message.from_user.id)
    await message.reply(
        text=text,
        reply_markup=reply_markup,
    )


@app.on_callback_query()
async def callback_query_handler(_, callback_query: CallbackQuery) -> None:
    """Обработчик inline кнопок."""
    task_id, option = callback_query.data.split('_')
    text, reply_markup = await bot_handler.filter_state(
        user_id=callback_query.from_user.id,
        option=option,
    )(task_id=int(task_id))
    await callback_query.message.reply(
        text=text,
        reply_markup=reply_markup,
    )


async def filter_state(_, __, message: Message) -> None | bool:
    """Фильтр для обработки button."""
    obj = bot_handler.filter_state(
        user_id=message.from_user.id,
        option=message.text,
    )
    if obj is None:
        return True

    result = await obj(
        message=message,
        text=message.text,
        user_id=message.from_user.id,
    )

    if not isinstance(result, tuple):
        return False

    text, reply_markup = result
    await message.reply(
        text=text,
        reply_markup=reply_markup,
    )


filter_fsm = filters.create(filter_state)


@app.on_message(filter_fsm)
async def handle_text(_, message: Message) -> None:
    """Обработчик любого входящего текста."""
    text, reply_markup = await bot_handler.handle_text()
    await message.reply(
        text=text,
        reply_markup=reply_markup,
    )


if __name__ == '__main__':
    app.run()
