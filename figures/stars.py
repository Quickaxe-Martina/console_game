import asyncio
import random

from _curses import window

from config import FRAMES
from tools.curses_tools import frame_sleep


async def blink(
    canvas: window,
    row: int,
    column: int,
    symbol: str = "*",
) -> None:
    """
    Мигает переданным символом на канве.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.
    row (int): Координата по вертикали, где нужно отобразить символ.
    column (int): Координата по горизонтали, где нужно отобразить символ.
    symbol (str, optional): Символ для отображения. По умолчанию "*".

    Returns:
    None
    """
    while True:
        # случайно выбираем показывать зажигать символ или нет
        if random.randint(0, 1):
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
        else:
            await asyncio.sleep(0)
