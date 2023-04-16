import asyncio

from config import TIC_TIMEOUT


def get_file_content(file_path: str) -> str:
    """
    Возвращает содержимое файла по переданному пути.

    Parameters:
    file_path (str): Путь к файлу.

    Returns:
    str: Содержимое файла.
    """
    with open(file_path, "r") as my_file:
        file_contents = my_file.read()
    return file_contents


async def sleep(time_sleep: float = 1.0) -> None:
    """
    Задерживает выполнение программы на указанное количество секунд.

    Parameters:
    time_sleep (float, optional): Время задержки в секундах. По умолчанию 1.0.

    Returns:
    None
    """
    for _ in range(int(time_sleep / TIC_TIMEOUT)):
        await asyncio.sleep(0)
