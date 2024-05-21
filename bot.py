import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.utils.chat_action import ChatActionSender
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from llm import AiSimpleClient
from config import bot_api_token

# All handlers should be attached to the Router (or Dispatcher)
router = Router()
bot = Bot(token=bot_api_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
llm = AiSimpleClient()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@router.message()
async def my_handler(message: Message) -> None:
    logging.info(f"Got message from {message}: {message.text}")
    ChatActionSender.typing(bot=bot, chat_id=message.chat.id)
    await message.answer(await reply_ai(message.text, message.chat.id))

async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    # And the run events dispatching
    await dp.start_polling(bot)

async def reply_ai(question: str, id) -> str:
    return await llm.reply(question, id)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())