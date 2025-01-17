import os
import img2pdf
from PIL import Image, ExifTags


__all__ = ['correct_orientation', 'compress_image', 'convert_images_in_directory_to_pdf']

def correct_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass

    return image


def compress_image(image_path, quality):
    image = Image.open(image_path)
    image = correct_orientation(image)
    compressed_image_path = f"compressed_{os.path.basename(image_path)}"
    image.save(compressed_image_path, "JPEG", quality=quality)
    return compressed_image_path


def convert_images_in_directory_to_pdf(directory_path, output_pdf, quality=75):
    # Получаем список файлов изображений в директории
    image_paths = sorted(
        [os.path.join(directory_path, f) for f in os.listdir(directory_path) if
         f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    )

    compressed_image_paths = [compress_image(image_path, quality) for image_path in image_paths]

    with open(output_pdf, "wb") as f:
        # Конвертируем изображения в PDF и сохраняем
        f.write(img2pdf.convert(compressed_image_paths))

    # Удаляем временные файлы
    for temp_image_path in compressed_image_paths:
        os.remove(temp_image_path)

    # print(f'PDF файл "{output_pdf}" успешно создан.')


# Пример использования
# directory_path = r'../../photos/id67171591'
# output_file = 'output.pdf'
# compression_quality = 75  # Процент качества сжатия
# convert_images_in_directory_to_pdf(directory_path, output_file, quality=compression_quality)
