import asyncio
import random
from typing import Coroutine

from _curses import window

from config import GARBAGE_PATH_FRAMES, MARGIN
from figures.explosion import explode
from globals import obstacles, obstacles_in_last_collisions
from tools.curses_tools import frame_sleep, get_frame_size
from tools.game_scenario import get_garbage_delay_tics
from tools.obstacles import Obstacle
from tools.tools import get_file_content


async def fill_orbit_with_garbage(canvas: window) -> None:
    """
    Заполнение орбиты мусором.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.

    Returns:
    None
    """
    # Получаем размеры канвы
    max_row, max_column = canvas.getmaxyx()

    # Загружаем кадры для отображения мусора
    frames = [get_file_content(garbage_path) for garbage_path in GARBAGE_PATH_FRAMES]

    # Вычисляем количество мусора
    max_frame_column = get_frame_size(max(frames, key=lambda x: get_frame_size(x)[1]))[
        1
    ]
    garbage_count = max_column // max_frame_column

    # Создаем пустой список корутин
    coroutines: list[Coroutine] = []
    tics_count = 0
    while True:
        delay_tics = get_garbage_delay_tics()

        if not delay_tics:
            await asyncio.sleep(0)
            continue
        # Обходим список корутин
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            # Удаляем корутину из списка при завершении выполнения корутины
            except StopIteration:
                coroutines.remove(coroutine)

        tics_count += 1
        if tics_count >= delay_tics:
            tics_count = 0
            r_frame = random.choice(frames)
            r_column = random.randint(MARGIN, max_column)
            coroutines.append(
                fly_garbage(
                    canvas=canvas,
                    column=r_column,
                    garbage_frame=r_frame,
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
    rows_size, columns_size = get_frame_size(garbage_frame)
    try:
        obstacle = Obstacle(
            row=0, column=column, rows_size=rows_size, columns_size=columns_size
        )
        obstacles.append(obstacle)

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
            obstacle.row = row - 1
            if obstacle in obstacles_in_last_collisions:
                return
    finally:
        obstacles.remove(obstacle)
        await explode(
            canvas=canvas,
            center_row=round(row + rows_size // 2),
            center_column=column + columns_size // 2,
        )
