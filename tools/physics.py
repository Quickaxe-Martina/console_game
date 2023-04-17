import math


def _limit(value: float, min_value: float, max_value: float) -> float:
    """
    Возвращает значение, ограниченное заданным диапазоном.

    Parameters:
    value (float): Значение, которое нужно ограничить.
    min_value (float): Нижняя граница диапазона.
    max_value (float): Верхняя граница диапазона.

    Returns:
    float: Значение, ограниченное заданным диапазоном.
    """
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def _apply_acceleration(
    speed: float, speed_limit: float, forward: bool = True
) -> float:
    """
    Применяет ускорение к скорости.

    Parameters:
    speed (float): Текущая скорость.
    speed_limit (float): Максимальное значение скорости.
    forward (bool, optional): Направление ускорения. Если True, то вперед, иначе назад.

    Returns:
    float: Новое значение скорости после применения ускорения.
    """
    speed_limit = abs(speed_limit)

    speed_fraction = speed / speed_limit

    # если корабль стоит на месте, дергаем резко
    # если корабль уже летит быстро, прибавляем медленно
    delta = math.cos(speed_fraction) * 0.75

    if forward:
        result_speed = speed + delta
    else:
        result_speed = speed - delta

    result_speed = _limit(result_speed, -speed_limit, speed_limit)

    # если скорость близка к нулю, то останавливаем корабль
    if abs(result_speed) < 0.1:
        result_speed = 0

    return result_speed


def update_speed(
    row_speed: float,
    column_speed: float,
    rows_direction: int,
    columns_direction: int,
    row_speed_limit: float = 2,
    column_speed_limit: float = 2,
    fading: float = 0.8,
) -> tuple[float, float]:
    """
    Обновляет скорость корабля в заданном направлении.

    Parameters:
    row_speed (float): Текущая скорость корабля по вертикали.
    column_speed (float): Текущая скорость корабля по горизонтали.
    rows_direction (int): Направление движения корабля по вертикали. Должно быть -1, 0 или 1.
    columns_direction (int): Направление движения корабля по горизонтали. Должно быть -1, 0 или 1.
    row_speed_limit (float, optional): Максимальная скорость корабля по вертикали. По умолчанию 2.
    column_speed_limit (float, optional): Максимальная скорость корабля по горизонтали. По умолчанию 2.
    fading (float, optional): Коэффициент затухания скорости. Должен быть от 0 до 1. По умолчанию 0.8.

    Returns:
    tuple[float, float]: Новое значение скорости корабля по вертикали и по горизонтали.
    """
    if rows_direction not in (-1, 0, 1):
        raise ValueError(
            f"Wrong rows_direction value {rows_direction}. Expects -1, 0 or 1."
        )

    if columns_direction not in (-1, 0, 1):
        raise ValueError(
            f"Wrong columns_direction value {columns_direction}. Expects -1, 0 or 1."
        )

    if fading < 0 or fading > 1:
        raise ValueError(
            f"Wrong columns_direction value {fading}. Expects float between 0 and 1."
        )

    # гасим скорость, чтобы корабль останавливался со временем
    row_speed *= fading
    column_speed *= fading

    row_speed_limit, column_speed_limit = abs(row_speed_limit), abs(column_speed_limit)

    if rows_direction != 0:
        row_speed = _apply_acceleration(row_speed, row_speed_limit, rows_direction > 0)

    if columns_direction != 0:
        column_speed = _apply_acceleration(
            column_speed, column_speed_limit, columns_direction > 0
        )

    return row_speed, column_speed
