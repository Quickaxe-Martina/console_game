import curses
import random
import time

from _curses import window

from config import MARGIN, ROCKET_COLUMN_SPEED, ROCKET_ROWS_SPEED, TIC_TIMEOUT
from figures.rocket import rocket
from figures.space_garbage import fill_orbit_with_garbage
from figures.stars import blink


def draw(canvas: window) -> None:
    """
    Основная функция отрисовки на канве.

    Parameters:
    canvas (SimpleCanvas): Канва, на которой происходит отрисовка.

    Returns:
    None
    """
    max_row, max_column = canvas.getmaxyx()
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)

    coroutine_lst = [
        blink(
            canvas=canvas,
            row=random.randint(MARGIN, max_row - MARGIN),
            column=random.randint(MARGIN, max_column - MARGIN),
            symbol=random.choice("+*.:"),
        )
        for _ in range(0, 100)
    ]

    coroutine_lst.append(
        rocket(
            canvas=canvas,
            start_row=max_row // 2,
            start_column=max_column // 2,
            rows_speed=ROCKET_ROWS_SPEED,
            columns_speed=ROCKET_COLUMN_SPEED,
        )
    )
    coroutine_lst.append(fill_orbit_with_garbage(canvas=canvas))

    while True:
        for coroutine in coroutine_lst:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutine_lst.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)
        if len(coroutine_lst) == 0:
            break


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
