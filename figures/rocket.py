from itertools import cycle

from _curses import window

from config import MARGIN, ROCKET_MARGIN, TIC_TIMEOUT
from figures.fire import fire
from figures.game_over import game_over
from globals import coroutine_lst, obstacles, year
from tools.curses_tools import frame_sleep, get_frame_size, read_controls
from tools.physics import update_speed
from tools.tools import get_file_content


async def rocket(
    canvas: window,
    start_row: int,
    start_column: int,
) -> None:
    """
    Анимация полета ракеты на канве.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.
    start_row (int): Начальная координата по вертикали.
    start_column (int): Начальная координата по горизонтали.

    Returns:
    None
    """
    # Загружаем кадры анимации ракеты
    rocket_frame_1 = get_file_content("frames/rocket/rocket_frame_1.txt")
    rocket_frame_2 = get_file_content("frames/rocket/rocket_frame_2.txt")

    # Устанавливаем начальную позицию ракеты
    row = start_row
    column = start_column

    # Устанавливаем начальную скорость ракеты
    rows_speed = columns_speed = 0

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
        rows_direction, columns_direction, space_pressed = read_controls(canvas=canvas)

        if space_pressed and year >= 2020:
            coroutine_lst.append(
                fire(
                    canvas=canvas,
                    start_row=row,
                    start_column=column,
                )
            )
            continue

        # Вычисляем скорость
        rows_speed, columns_speed = update_speed(
            row_speed=rows_speed,
            column_speed=columns_speed,
            rows_direction=rows_direction,
            columns_direction=columns_direction,
        )

        # Вычисляем новую позицию ракеты
        row_new = row + rows_speed
        column_new = column + columns_speed

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

        # проверка столкновения ракеты с мусором
        for obstacle in obstacles:
            if obstacle.has_collision(
                obj_corner_row=row,
                obj_corner_column=column,
                obj_size_rows=frame_rows,
                obj_size_columns=frame_columns,
            ):
                await game_over(canvas=canvas)
                return

        # Отображаем кадр анимации на канве
        await frame_sleep(
            canvas=canvas,
            row=row,
            column=column,
            text=frame,
            time_sleep=TIC_TIMEOUT * 2,
        )
