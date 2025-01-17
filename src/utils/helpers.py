from datetime import datetime
import os

from aiogram import Bot

__all__ = ['timer_left_format', 'save_photo', 'delete_output', 'delete_input', 'makedirs_for_new_user']


def timer_left_format(time_left: float) -> str:
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    return f'{minutes} мин {seconds} сек'

async def save_photo(bot: Bot,
                     message_id: int,
                     user_id: int,
                     photo_id: str) -> None:
    directory = f'photos/id{user_id}'
    filename = message_id
    os.makedirs(directory, exist_ok=True)
    file_info = await bot.get_file(photo_id)
    file_path = file_info.file_path  # Загрузка файла и сохранение его в созданную директорию
    await bot.download_file(file_path, f'{directory}/{filename}.png')
    print(f'Фото сохранено в директорию: {directory}/{filename}.png')


async def makedirs_for_new_user(user_id: int):
    photo_directory = f'photos/id{user_id}'
    pdf_directory = f'pdfs/id{user_id}'
    os.makedirs(photo_directory, exist_ok=True)
    os.makedirs(pdf_directory, exist_ok=True)


def delete_output(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
        print(f'Файл {path} был удален.')
    else:
        print(f'Файл {path} не найден.')


def delete_input(path: str):
    image_paths = sorted(
        [os.path.join(path, f) for f in os.listdir(path) if
         f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    )
    for file in image_paths:
        if os.path.exists(file):
            os.remove(file)
            print(f'Файл {file} был удален')
        else:
            print(f'Файл {file} не найден')