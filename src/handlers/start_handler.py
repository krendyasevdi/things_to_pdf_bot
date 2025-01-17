from aiogram import types, Router
from aiogram.filters import CommandStart
from ..services.database_functions import add_user, get_user
from ..utils.helpers import makedirs_for_new_user

from datetime import datetime

start_router = Router()


@start_router.message(CommandStart())
async def start_command(message: types.Message):
    user = get_user(message.from_user.id)
    if user is None:
        add_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            loading_file=0
        )
        await makedirs_for_new_user(message.from_user.id)
        await message.answer("Добро пожаловать! Вы успешно зарегистрированы.")
    else:
        await message.answer(f"Рады видеть вас снова, {message.from_user.first_name}!")
