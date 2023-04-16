import curses

TIC_TIMEOUT: float = 0.1
MARGIN: int = 2

FRAMES: list[tuple[float, int]] = [
    (2.0, curses.A_DIM),
    (0.3, curses.A_NORMAL),
    (0.5, curses.A_BOLD),
    (0.3, curses.A_NORMAL),
]

ROCKET_ROWS_SPEED: int = 1
ROCKET_COLUMN_SPEED: int = 5
ROCKET_MARGIN: int = 1
