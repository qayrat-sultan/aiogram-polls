import admin_commands
import configs
import handlers

from aiogram import types
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage

BOT_TOKEN = configs.BOT_TOKEN
bot = Bot(token=configs.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class SetReport(StatesGroup):
    report = State()


class SetPoll(StatesGroup):
    poll = State()


@dp.message_handler(commands=["start"])
async def start_menu(message: types.Message):
    await handlers.start_menu_handler(message)


@dp.message_handler(commands=["main"])
async def menu(message: types.Message):
    await handlers.menu_handler(message)


@dp.message_handler(commands=['post'])
async def post(message: types.Message):
    data = {'type': 'text', 'text': 'text', 'entities': None}
    users = 390736292,
    await admin_commands.send_post_all_users(data, users, bot)


@dp.message_handler(commands=["report"])
async def report(message: types.Message):
    await SetReport.report.set()
    await message.answer("Bizga o'z takliflaringizni yuboring!")


@dp.message_handler(state=SetReport.report,
                    content_types=configs.all_content_types)
async def report_process(message: types.Message, state: FSMContext):
    await handlers.report_process_handler(message, state)


@dp.message_handler(content_types=configs.all_content_types)
async def some_text(message: types.Message):
    await handlers.some_text_handler(message)


@dp.poll_answer_handler()
async def poll_answers(poll_answer: types.PollAnswer):
    await handlers.poll_answers_handler(poll_answer)


if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=configs.on_startup,
                           on_shutdown=configs.on_shutdown)
