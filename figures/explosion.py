import curses

from _curses import window

from tools.curses_tools import frame_sleep, get_frame_size

EXPLOSION_FRAMES: list[tuple[float, str]] = [
    (
        0.3,
        """\
           (_)
       (  (   (  (
      () (  (  )
        ( )  ()
    """,
    ),
    (
        0.3,
        """\
           (_)
       (  (   (
         (  (  )
          )  (
    """,
    ),
    (
        0.3,
        """\
            (
          (   (
         (     (
          )  (
    """,
    ),
    (
        0.3,
        """\
            (
              (
            (
    """,
    ),
]


async def explode(canvas: window, center_row: int, center_column: int) -> None:
    """
    Анимированное отображение взрыва на канвасе с использованием библиотеки curses.

    Args:
    canvas (window): Канвас для отображения.
    center_row (float): Центральная позиция строки.
    center_column (float): Центральная позиция столбца.

    Returns:
    None
    """
    rows, columns = get_frame_size(EXPLOSION_FRAMES[0][1])
    corner_row = round(center_row - rows / 2)
    corner_column = round(center_column - columns / 2)

    curses.beep()
    for time_sleep, frame in EXPLOSION_FRAMES:
        await frame_sleep(
            canvas=canvas,
            row=corner_row,
            column=corner_column,
            text=frame,
            time_sleep=time_sleep,
        )
