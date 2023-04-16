import curses
import random
import time

from _curses import window

from config import DEBUG, MARGIN, TIC_TIMEOUT
from figures.rocket import rocket
from figures.space_garbage import fill_orbit_with_garbage
from figures.stars import blink
from globals import coroutine_lst, obstacles
from tools.game_scenario import year_timer
from tools.obstacles import show_obstacles


def draw(canvas: window) -> None:
    """
    Основная функция отрисовки на канве.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.

    Returns:
    None
    """
    max_row, max_column = canvas.getmaxyx()
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    info_table = canvas.derwin(max_row - 2, 1)

    for _ in range(0, 100):
        coroutine_lst.append(
            blink(
                canvas=canvas,
                row=random.randint(MARGIN, max_row - MARGIN),
                column=random.randint(MARGIN, max_column - MARGIN),
                symbol=random.choice("+*.:"),
            )
        )

    coroutine_lst.append(
        rocket(
            canvas=canvas,
            start_row=max_row // 2,
            start_column=max_column // 2,
        )
    )
    coroutine_lst.append(year_timer(info_table))
    coroutine_lst.append(fill_orbit_with_garbage(canvas=canvas))
    if DEBUG:
        coroutine_lst.append(show_obstacles(canvas=canvas, obstacles=obstacles))

    while True:
        for coroutine in coroutine_lst:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutine_lst.remove(coroutine)
        canvas.refresh()
        info_table.refresh()
        time.sleep(TIC_TIMEOUT)
        if len(coroutine_lst) == 0:
            break


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
