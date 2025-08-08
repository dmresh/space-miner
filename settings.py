from dataclasses import dataclass
from enum import UNIQUE, Enum, auto, verify


@verify(UNIQUE)
class AppEvents(Enum):
    no_event = auto()
    go_to_the_game = auto()
    go_to_main_menu = auto()
    go_to_pause_menu = auto()
    go_to_shop_menu = auto()
    quit_the_game = auto()


@dataclass
class Settings:
    screen_size_x: int = 1400
    screen_size_y: int = 900
    screen_size: tuple[int, int] = screen_size_x, screen_size_y
    screen_center: tuple[int, int] = screen_size_x // 2, screen_size_y // 2
    asteroids_start_amount: int = 2
    safe_distance: int = 100


@dataclass
class Prices:
    bullets: int = 2000
    lives: int = 10000


@dataclass
class DefaultStats:
    level: int = 1
    credits: int = 0
    lives: int = 3
    max_bullets: int = 21


@dataclass
class UserStats:
    level: int = DefaultStats.level
    credits: int = DefaultStats.credits
    lives: int = DefaultStats.lives
    max_bullets: int = DefaultStats.max_bullets


@dataclass
class Colors:
    black = (0, 0, 0)
    blue = (60, 60, 255)
    blue_dark = (30, 30, 120)
    blue_darker = (10, 10, 30)
    gray = (200, 200, 200)
    green = (60, 255, 60)
    green_dark = (30, 120, 30)
    green_acidic = (100, 255, 0)
    red = (255, 60, 60)
    yellow = (255, 255, 0)
    white = (255, 255, 255)
