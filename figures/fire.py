import asyncio
import curses

from _curses import window

from globals import obstacles, obstacles_in_last_collisions


async def fire(
    canvas: window,
    start_row: int,
    start_column: int,
    rows_speed: float = -0.3,
    columns_speed: float = 0,
) -> None:
    """
    Анимация выстрела.

    Parameters:
    canvas (window): Канва, на которой происходит отрисовка.
    start_row (float): Начальная позиция строки.
    start_column (float): Начальная позиция столбца.
    rows_speed (float): Скорость движения по вертикали.
    columns_speed (float): Скорость движения по горизонтали.

    Returns:
    None
    """
    # Инициализация начальных значений позиции огня
    row, column = start_row, start_column

    # Отображение символа '*' на канвасе в начальной позиции
    canvas.addstr(round(row), round(column), "*")
    await asyncio.sleep(0)

    # Затухание символа '*'
    canvas.addstr(round(row), round(column), "O")
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), " ")

    # Перемещение позиции выстрела
    row += rows_speed
    column += columns_speed

    # Выбор символа для отображения огня в зависимости от скорости движения по горизонтали
    symbol = "-" if columns_speed else "|"

    # Получение размеров канваса
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    # Звуковой сигнал
    curses.beep()

    # Отображение огня на канвасе в новой позиции
    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), " ")
        for obstacle in obstacles:
            if obstacle.has_collision(obj_corner_row=row, obj_corner_column=column):
                obstacles_in_last_collisions.append(obstacle)
                return
        row += rows_speed
        column += columns_speed
