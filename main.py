import asyncio
import curses
import random
import time
from itertools import cycle

from _curses import window

from config import (
    FRAMES,
    MARGIN,
    ROCKET_COLUMN_SPEED,
    ROCKET_MARGIN,
    ROCKET_ROWS_SPEED,
    TIC_TIMEOUT,
)
from curses_tools import draw_frame, get_frame_size, read_controls


async def blink(
    canvas: window,
    row: int,
    column: int,
    symbol: str = "*",
):
    while True:
        if random.randint(0, 1):
            for time_sleep, style in FRAMES:
                for _ in range(int(time_sleep * 10)):
                    canvas.addstr(row, column, symbol, style)
                    await asyncio.sleep(0)
        else:
            await asyncio.sleep(0)


async def rocket(
    canvas: window,
    start_row: int,
    start_column: int,
    rows_speed: int = 1,
    columns_speed: int = 1,
):
    rocket_frame_1 = get_file_content("rocket_frame_1.txt")
    rocket_frame_2 = get_file_content("rocket_frame_2.txt")

    row = start_row
    column = start_column

    for clear_frame, frame in cycle(
        (
            (rocket_frame_2, rocket_frame_1),
            (rocket_frame_1, rocket_frame_2),
        )
    ):
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=clear_frame,
            negative=True,
        )

        max_row, max_column = canvas.getmaxyx()
        max_row -= ROCKET_MARGIN
        max_column -= ROCKET_MARGIN + MARGIN

        rows_direction, columns_direction, _ = read_controls(canvas=canvas)
        row_new = row + rows_direction * rows_speed
        column_new = column + columns_direction * columns_speed
        frame_rows, frame_columns = get_frame_size(text=frame)

        if not (ROCKET_MARGIN > row_new or max_row < row_new + frame_rows):
            row = row_new
        elif ROCKET_MARGIN > row_new:
            row = ROCKET_MARGIN
        elif max_row < row_new + frame_rows:
            row = max_row - frame_rows

        if not (ROCKET_MARGIN > column_new or max_column < column_new + frame_columns):
            column = column_new
        elif ROCKET_MARGIN > column_new:
            column = ROCKET_MARGIN
        elif max_column < column_new + frame_columns:
            column = max_column - frame_columns

        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=frame,
            negative=False,
        )
        await asyncio.sleep(0)


def get_file_content(file_path: str) -> str:
    with open(file_path, "r") as my_file:
        file_contents = my_file.read()
    return file_contents


def draw(canvas: window):
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
