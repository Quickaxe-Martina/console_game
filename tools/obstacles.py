import asyncio
from typing import Any, Generator, Optional

from _curses import window

from tools.curses_tools import draw_frame


class Obstacle:
    def __init__(
        self,
        row: int,
        column: int,
        rows_size: int = 1,
        columns_size: int = 1,
        uid: Optional[int] = None,
    ):
        """
        Конструктор класса препятствия

        Args:
        row (int): координата строки, где находится верхний левый угол препятствия
        column (int): координата столбца, где находится верхний левый угол препятствия
        rows_size (int): высота препятствия в строках
        columns_size (int): ширина препятствия в столбцах
        uid (int): уникальный идентификатор препятствия
        """
        self.row = row
        self.column = column
        self.rows_size = rows_size
        self.columns_size = columns_size
        self.uid = uid

    def get_bounding_box_frame(self) -> str:
        """
        Возвращает рамку, ограничивающую препятствие

        Returns:
        str: рамка, ограничивающая препятствие
        """
        rows, columns = self.rows_size + 1, self.columns_size + 1
        return "\n".join(_get_bounding_box_lines(rows, columns))

    def get_bounding_box_corner_pos(self) -> tuple[int, int]:
        """
        Возвращает координаты верхнего левого угла рамки, ограничивающей препятствие

        Returns:
        tuple[int, int]: координаты верхнего левого угла рамки, ограничивающей препятствие
        """
        return self.row - 1, self.column - 1

    def dump_bounding_box(self) -> tuple[int, int, str]:
        """
        Возвращает кортеж, содержащий координаты верхнего левого угла рамки, ограничивающей препятствие, и саму рамку

        Returns:
        tuple[int, int, str]: кортеж, содержащий координаты верхнего левого угла рамки, ограничивающей препятствие, и саму рамку
        """
        row, column = self.get_bounding_box_corner_pos()
        return row, column, self.get_bounding_box_frame()

    def has_collision(
        self,
        obj_corner_row: int,
        obj_corner_column: int,
        obj_size_rows: int = 1,
        obj_size_columns: int = 1,
    ) -> bool:
        """
        Определяет, произошло ли столкновение с препятствием

        Args:
        obj_corner_row (int): координата строки, где находится верхний левый угол
        obj_corner_column (int): координата столбца, где находится верхний левый угол
        obj_size_rows (int): высота объекта в строках
        obj_size_columns (int): ширина объекта в столбцах

        Returns:
        bool: True, если столкновение произошло, False - иначе
        """
        return has_collision(
            (self.row, self.column),
            (self.rows_size, self.columns_size),
            (obj_corner_row, obj_corner_column),
            (obj_size_rows, obj_size_columns),
        )


def _get_bounding_box_lines(rows: int, columns: int) -> Generator[str, Any, None]:
    """
    Возвращает список строк, соответствующих рамке

    Args:
    rows (int): количество строк в рамке
    columns (int): количество столбцов в рамке

    Returns:
    str: список строк, соответствующих рамке
    """
    yield " " + "-" * columns + " "
    for _ in range(rows):
        yield "|" + " " * columns + "|"
    yield " " + "-" * columns + " "


async def show_obstacles(canvas: window, obstacles: list[Obstacle]) -> None:
    """
    Отображает рамки, ограничивающие каждое препятствие в списке

    Args:
    canvas (window): Канва, на которой происходит отрисовка.
    obstacles (list[Obstacle]): список препятствий
    Returns:
    None
    """

    while True:
        boxes = []

        for obstacle in obstacles:
            boxes.append(obstacle.dump_bounding_box())

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame)

        await asyncio.sleep(0)

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame, negative=True)


def _is_point_inside(
    corner_row: int,
    corner_column: int,
    size_rows: int,
    size_columns: int,
    point_row: int,
    point_row_column: int,
) -> bool:
    """
    Определяет, находится ли точка внутри прямоугольника

    Args:
    corner_row (int): координата строки, где находится верхний левый угол прямоугольника
    corner_column (int): координата столбца, где находится верхний левый угол прямоугольника
    size_rows (int): высота прямоугольника в строках
    size_columns (int): ширина прямоугольника в столбцах
    point_row (int): координата строки точки
    point_row_column (int): координата столбца точки

    Returns:
    bool: True, если точка находится внутри прямоугольника, False - иначе
    """
    rows_flag = corner_row <= point_row < corner_row + size_rows
    columns_flag = corner_column <= point_row_column < corner_column + size_columns

    return rows_flag and columns_flag


def has_collision(
    obstacle_corner: tuple[int, int],
    obstacle_size: tuple[int, int],
    obj_corner: tuple[int, int],
    obj_size: tuple[int, int] = (1, 1),
) -> bool:
    """
    Определяет, произошло ли столкновение двух прямоугольников

    Args:
    obstacle_corner (tuple[int, int]): координаты верхнего левого угла первого прямоугольника
    obstacle_size (tuple[int, int]): размеры первого прямоугольника
    obj_corner (tuple[int, int]): координаты верхнего левого угла второго прямоугольника
    obj_size (tuple[int, int]): размеры второго прямоугольника (по умолчанию (1, 1))

    Returns:
    bool: True, если столкновение произошло, False - иначе
    """

    opposite_obstacle_corner = (
        obstacle_corner[0] + obstacle_size[0] - 1,
        obstacle_corner[1] + obstacle_size[1] - 1,
    )

    opposite_obj_corner = (
        obj_corner[0] + obj_size[0] - 1,
        obj_corner[1] + obj_size[1] - 1,
    )

    return any(
        [
            _is_point_inside(*obstacle_corner, *obstacle_size, *obj_corner),
            _is_point_inside(*obstacle_corner, *obstacle_size, *opposite_obj_corner),
            _is_point_inside(*obj_corner, *obj_size, *obstacle_corner),
            _is_point_inside(*obj_corner, *obj_size, *opposite_obstacle_corner),
        ]
    )
