from typing import Coroutine

from tools.obstacles import Obstacle

coroutine_lst: list[Coroutine] = []
# список с препятствиями
obstacles: list[Obstacle] = []
# список с препятствиями, по которым попали выстрелы
obstacles_in_last_collisions: list[Obstacle] = []
# год
year: int = 1957

debug_objects: list[str] = ["DEBUG=True"]
