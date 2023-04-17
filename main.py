import asyncio
import curses
import random
import time
from itertools import cycle
from typing import Coroutine

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
    canvas: window, row: int, column: int, symbol: str = "*", offset_tics: int = 1
):
    while True:
        for _ in range(offset_tics):
            await asyncio.sleep(0)
        for time_sleep, style in FRAMES:
            for _ in range(int(time_sleep * 10)):
                canvas.addstr(row, column, symbol, style)
                await asyncio.sleep(0)


async def move_rocket(
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

    for frame in cycle(
        (
            rocket_frame_1,
            rocket_frame_1,
            rocket_frame_2,
            rocket_frame_2,
        )
    ):
        max_row, max_column = canvas.getmaxyx()
        max_row -= ROCKET_MARGIN
        max_column -= ROCKET_MARGIN + MARGIN

        rows_direction, columns_direction, _ = read_controls(canvas=canvas)
        row_new = row + rows_direction * rows_speed
        column_new = column + columns_direction * columns_speed
        frame_rows, frame_columns = get_frame_size(text=frame)

        row = min(max(ROCKET_MARGIN, row_new), max_row - frame_rows)
        column = min(max(ROCKET_MARGIN, column_new), max_column - frame_columns)

        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=frame,
            negative=False,
        )
        await asyncio.sleep(0)
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=frame,
            negative=True,
        )


def get_file_content(file_path: str) -> str:
    with open(file_path, "r") as my_file:
        file_contents = my_file.read()
    return file_contents


def draw(canvas: window):
    max_row, max_column = canvas.getmaxyx()
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)

    coroutine_lst: list[Coroutine] = [
        blink(
            canvas=canvas,
            row=random.randint(MARGIN, max_row - MARGIN),
            column=random.randint(MARGIN, max_column - MARGIN),
            symbol=random.choice("+*.:"),
            offset_tics=random.randint(1, 10),
        )
        for _ in range(0, 100)
    ]

    coroutine_lst.append(
        move_rocket(
            canvas=canvas,
            start_row=max_row // 2,
            start_column=max_column // 2,
            rows_speed=ROCKET_ROWS_SPEED,
            columns_speed=ROCKET_COLUMN_SPEED,
        )
    )

    while True:
        for coroutine in coroutine_lst.copy():
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
