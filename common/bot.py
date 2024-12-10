from pyrogram import Client, enums

from common.settings import settings

app = Client(
    name=settings.NAME_BOT,
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN,
    parse_mode=enums.ParseMode.MARKDOWN,
)
