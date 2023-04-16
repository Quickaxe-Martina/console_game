from itertools import cycle

from _curses import window

from config import MARGIN, ROCKET_MARGIN, TIC_TIMEOUT
from tools.curses_tools import frame_sleep, get_frame_size, read_controls
from tools.tools import get_file_content


async def rocket(
    canvas: window,
    start_row: int,
    start_column: int,
    rows_speed: int = 1,
    columns_speed: int = 3,
) -> None:
    """
    Анимация полета ракеты на канве.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.
    start_row (int): Начальная координата по вертикали.
    start_column (int): Начальная координата по горизонтали.
    rows_speed (int, optional): Скорость перемещения по вертикали. По умолчанию 1.
    columns_speed (int, optional): Скорость перемещения по горизонтали. По умолчанию 3.

    Returns:
    None
    """
    # Загружаем кадры анимации ракеты
    rocket_frame_1 = get_file_content("frames/rocket/rocket_frame_1.txt")
    rocket_frame_2 = get_file_content("frames/rocket/rocket_frame_2.txt")

    # Устанавливаем начальную позицию ракеты
    row = start_row
    column = start_column

    # Запускаем бесконечный цикл, в котором будут меняться кадры анимации
    for frame in cycle(
        (
            rocket_frame_1,
            rocket_frame_2,
        )
    ):
        # Получаем максимальное количество строк и столбцов на канве
        max_row, max_column = canvas.getmaxyx()

        # Учитываем отступы для ракеты
        max_row -= ROCKET_MARGIN
        max_column -= ROCKET_MARGIN + MARGIN

        # Получаем направление движения по осям
        rows_direction, columns_direction, _ = read_controls(canvas=canvas)

        # Вычисляем новую позицию ракеты
        row_new = row + rows_direction * rows_speed
        column_new = column + columns_direction * columns_speed

        # Получаем размеры текущего кадра анимации
        frame_rows, frame_columns = get_frame_size(text=frame)

        # Обрабатываем граничные условия для движения ракеты
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

        # Отображаем кадр анимации на канве
        await frame_sleep(
            canvas=canvas,
            row=row,
            column=column,
            text=frame,
            time_sleep=TIC_TIMEOUT,
        )
