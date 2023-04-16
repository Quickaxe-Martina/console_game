import asyncio
import curses

from _curses import window

from config import TIC_TIMEOUT

SPACE_KEY_CODE: int = 32
LEFT_KEY_CODE: int = 260
RIGHT_KEY_CODE: int = 261
UP_KEY_CODE: int = 259
DOWN_KEY_CODE: int = 258


def read_controls(canvas: window) -> tuple[int, int, bool]:
    """
    Читает нажатия клавиш управления.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.

    Returns:
    tuple[int, int, bool]: Кортеж из направления движения корабля по вертикали,
        направления движения корабля по горизонтали и флага нажатия пробела.
    """
    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def draw_frame(
    canvas: window,
    start_row: int,
    start_column: int,
    text: str,
    negative: bool = False,
    style: int = curses.A_NORMAL,
) -> None:
    """
    Рисует на канве заданный фрейм.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.
    start_row (int): Начальная координата по вертикали.
    start_column (int): Начальная координата по горизонтали.
    text (str): Строка с текстом для отображения.
    negative (bool, optional): Флаг, указывающий, нужно ли стереть фрейм. По умолчанию False.
    style (int, optional): Стиль отображения символов. По умолчанию curses.A_NORMAL.

    Returns:
    None
    """
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == " ":
                continue

            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else " "
            canvas.addch(row, column, symbol, style)


def get_frame_size(text: str) -> tuple[int, int]:
    """
    Вычисляет размер фрейма по переданному тексту.

    Parameters:
    text (str): Строка с текстом для отображения.

    Returns:
    tuple[int, int]: Кортеж из количества строк и колонок в фрейме.
    """
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


async def frame_sleep(
    canvas: window,
    row: int,
    column: int,
    text: str,
    style: int = curses.A_NORMAL,
    time_sleep: float = 1.0,
) -> None:
    """
    Задерживает выполнение программы на указанное количество секунд и отображает переданный фрейм на канве.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.
    row (int): Координата по вертикали, где нужно отобразить фрейм.
    column (int): Координата по горизонтали, где нужно отобразить фрейм.
    text (str): Строка с текстом для отображения.
    style (int, optional): Стиль отображения символов. По умолчанию curses.A_NORMAL.
    time_sleep (float, optional): Время задержки в секундах. По умолчанию 1.0.

    Returns:
    None
    """
    for _ in range(int(time_sleep / TIC_TIMEOUT)):
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=text,
            style=style,
        )
        await asyncio.sleep(0)
        draw_frame(
            canvas=canvas,
            start_row=row,
            start_column=column,
            text=text,
            negative=True,
        )


async def debug_log(canvas: window):
    from globals import debug_objects

    while True:
        await frame_sleep(
            canvas=canvas,
            row=0,
            column=0,
            text="\n".join(debug_objects),
            style=curses.color_pair(1) | curses.A_BOLD,
            time_sleep=TIC_TIMEOUT,
        )
        canvas.refresh()
