import curses

from _curses import window

from config import TIC_TIMEOUT
from tools.curses_tools import frame_sleep, get_frame_size

FRAME = """
   _____                         ____                 
  / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
                                                      
                                                      
"""


async def game_over(canvas: window) -> None:
    """
    Отображение сообщения об окончании игры на канвасе с использованием библиотеки curses.

    Args:
    canvas (window): Канвас для отображения.

    Returns:
    None
    """
    # Получение размеров канваса и сообщения об окончании игры
    max_row, max_column = canvas.getmaxyx()
    size_row, size_column = get_frame_size(FRAME)

    # Вычисление начальной позиции для отображения сообщения
    row = max_row // 2 - size_row // 2
    column = max_column // 2 - size_column // 2

    # Отображение сообщения об окончании игры на канвасе
    while True:
        await frame_sleep(
            canvas=canvas,
            row=row,
            column=column,
            text=FRAME,
            style=curses.color_pair(1) | curses.A_BOLD,
            time_sleep=TIC_TIMEOUT,
        )
