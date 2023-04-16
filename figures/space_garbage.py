import asyncio
import random
from typing import Coroutine

from _curses import window

from config import GARBAGE_PATH_FRAMES, MARGIN
from tools.curses_tools import frame_sleep
from tools.tools import get_file_content


async def fill_orbit_with_garbage(canvas: window) -> None:
    """
    Заполнение орбиты мусором.

    Parameters:
    canvas (SimpleCanvas): Канва, на которой происходит отрисовка.

    Returns:
    None
    """
    # Получаем размеры канвы
    max_row, max_column = canvas.getmaxyx()

    # Вычисляем количество мусора
    garbage_count = max_column // 10

    # Загружаем кадры для отображения мусора
    frames = [get_file_content(garbage_path) for garbage_path in GARBAGE_PATH_FRAMES]

    # Создаем пустой список корутин
    coroutine_lst: list[Coroutine] = []
    while True:
        # Обходим список корутин
        for coroutine in coroutine_lst:
            try:
                coroutine.send(None)
            # Удаляем корутину из списка при завершении выполнения корутины
            except StopIteration:
                coroutine_lst.remove(coroutine)
        # Проверяем нужно ли добавлять новый мусор
        if garbage_count != len(coroutine_lst):
            # случайно выбираем добавить или нет
            if random.randint(0, 1):
                coroutine_lst.append(
                    fly_garbage(
                        canvas=canvas,
                        column=random.randint(MARGIN, max_column),
                        garbage_frame=random.choice(frames),
                    )
                )
        await asyncio.sleep(0)


async def fly_garbage(
    canvas: window,
    column: int,
    garbage_frame: str,
    speed: float = 0.5,
) -> None:
    """
    Анимация полета мусора на канве.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.
    column (int): Координата по горизонтали, где должен появиться мусор.
    garbage_frame (str): Строка с текстом для отображения мусора.
    speed (float, optional): Скорость полета мусора. По умолчанию 0.5.

    Returns:
    None
    """
    # Получаем размеры канвы
    rows_number, columns_number = canvas.getmaxyx()

    row = 0.0

    # Цикл анимации движения мусора по экрану
    while row < rows_number:
        await frame_sleep(
            canvas=canvas,
            row=round(row),
            column=column,
            text=garbage_frame,
            time_sleep=1.0 / speed,
        )
        row += speed
