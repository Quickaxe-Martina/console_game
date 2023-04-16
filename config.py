import curses

# Время в секундах между кадрами игры, оно используется для ограничения количества обновлений экрана
# и поддержания похожести на 60 кадров в секунду.
TIC_TIMEOUT: float = 1.0 / 60.0

# Отступ от краев экрана, который используется для размещения объектов игры внутри игрового поля.
MARGIN: int = 2

# Список временных интервалов и стилей, используемых для анимации мерцания звезд.
FRAMES: list[tuple[float, int]] = [
    (2.0, curses.A_DIM),
    (0.3, curses.A_NORMAL),
    (0.5, curses.A_BOLD),
    (0.3, curses.A_NORMAL),
]

# Скорость движения космического корабля вверх и вниз на экране.
ROCKET_ROWS_SPEED: int = 1
# Скорость движения космического корабля вправо и влево на экране.
ROCKET_COLUMN_SPEED: int = 1
# Отступ от краев экрана, используемый для размещения космического корабля внутри игрового поля.
ROCKET_MARGIN: int = 1

# Список путей к файлам с изображениями космического мусора,
# которые используются в игре для создания анимации летящих объектов.
GARBAGE_PATH_FRAMES = [
    "frames/garbage/duck.txt",
    "frames/garbage/hubble.txt",
    "frames/garbage/lamp.txt",
    "frames/garbage/trash_large.txt",
    "frames/garbage/trash_small.txt",
    "frames/garbage/trash_xl.txt",
]
