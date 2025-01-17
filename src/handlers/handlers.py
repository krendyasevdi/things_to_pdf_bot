from tokenize import group

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from ..utils.constant_messages import *
from ..utils.helpers import *
from ..services.database_functions import *
from ..services.timer import *
from ..services.to_pdf import *

# from ..utils.helpers import save_photo, get_names_by_now

router = Router()


def dummy_func():
    pass


timer = CountdownTimer(1800, dummy_func)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=help_message,
                         parse_mode=ParseMode.HTML)


@router.message(Command(commands='start_photo_load'))
async def process_start_photo_load_command(message: Message):
    status = get_loading_status(message.from_user.id)
    if not status:
        await timer.start()
        change_loading_photo_status(message.from_user.id)
        await message.answer('Вы начали загрузку изображений, успевайте за полчаса.')
    else:
        await message.answer(already_loading)


@router.message(Command(commands=['ghj']))
async def dummy(message: Message):
    change_loading_photo_status(message.from_user.id)
    await message.answer('Ваш статус изменен')


@router.message(Command(commands='check_timer'))
async def check_timer(message: Message):
    if timer and timer.time_left() != 0:
        time_left = timer.time_left()
        time_left_message = timer_left_format(time_left)
        await message.answer(text=f'Осталось {time_left_message}')
    else:
        await message.answer(text=timer_not_set)


@router.message(Command(commands='end_photo_load'))
async def process_end_photo_load_command(message: Message):
    status = get_loading_status(message.from_user.id)
    if not status:
        await message.answer(photo_load_not_started)
    else:
        timer.cancel()
        change_loading_photo_status(message.from_user.id)
        await message.answer(photo_load_ended)
        directory_path = f'photos/id{message.from_user.id}'
        file_path = f'pdfs/id{message.from_user.id}/output.pdf'
        convert_images_in_directory_to_pdf(directory_path, file_path)
        await message.bot.send_document(chat_id=message.from_user.id,
                                        document=FSInputFile(path=file_path))
        delete_output(file_path)
        delete_input(directory_path)


# /Users/krendyasev/Documents/Python/python_to_pdf/python_to_pdf/photos/id67171591
@router.message(F.photo)
async def catch_photo(message: Message):
    status = get_loading_status(message.from_user.id)
    media_group_id = message.media_group_id
    if status:
        await save_photo(message.bot,
                         message.message_id,
                         message.from_user.id,
                         message.photo[-1].file_id
                         )
    else:
        # if media_group_id and media_group_id not in group_tracker:
            # group_tracker.add(message.message_id)
        await message.answer(send_photo_but_not_started_loading)
        # await message.answer(f'ID группы: {message.media_group_id}')
