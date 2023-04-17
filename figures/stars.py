import asyncio
import random

from _curses import window

from config import FRAMES
from tools.curses_tools import frame_sleep


async def blink(
    canvas: window, row: int, column: int, symbol: str = "*", offset_tics: int = 1
) -> None:
    """
    Мигает переданным символом на канве.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.
    row (int): Координата по вертикали, где нужно отобразить символ.
    column (int): Координата по горизонтали, где нужно отобразить символ.
    symbol (str, optional): Символ для отображения. По умолчанию "*".
    offset_tics (int): Задержка перед началом анимации

    Returns:
    None
    """
    while True:
        # случайно выбираем показывать зажигать символ или нет
        for _ in range(offset_tics):
            await asyncio.sleep(0)
        # проходим по фреймам из списка FRAMES
        for time_sleep, style in FRAMES:
            await frame_sleep(
                canvas=canvas,
                row=row,
                column=column,
                text=symbol,
                style=style,
                time_sleep=time_sleep,
            )
