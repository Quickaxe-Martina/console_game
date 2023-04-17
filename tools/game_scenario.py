import curses
from typing import Optional

from _curses import window

from config import PHRASES
from globals import year
from tools.curses_tools import draw_frame, frame_sleep


def get_garbage_delay_tics() -> Optional[int]:
    """
    Возвращает количество тиков задержки между появлением мусора на экране в зависимости от года.

    Args:
    year (int): Год.

    Returns:
    Optional[int]: Количество тиков задержки между появлением мусора на экране.
            Возвращает `None`, если год меньше 1961.
    """
    if year < 1961:
        return None
    elif year < 1969:
        return 200
    elif year < 1981:
        return 140
    elif year < 1995:
        return 100
    elif year < 2010:
        return 80
    elif year < 2020:
        return 60
    else:
        return 20


async def year_timer(canvas: window) -> None:
    """
    Анимированное отображение таймера года на канвасе с использованием библиотеки curses.

    Args:
    canvas (window): Канвас для отображения.

    Returns:
    None
    """
    global year

    while True:
        await frame_sleep(
            canvas=canvas,
            row=0,
            column=0,
            text=f"{year=} {PHRASES.get(year, '')}",
            style=curses.color_pair(1) | curses.A_BOLD,
            time_sleep=1.5,
        )
        year += 1
