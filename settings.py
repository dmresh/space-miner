from dataclasses import dataclass
from typing import Tuple


@dataclass
class AppEvents:
    go_to_the_game: str = 'go to the game'
    go_to_main_menu: str = 'go to main menu'
    go_to_pause_menu: str = 'go to pause menu'
    go_to_shop_menu: str = 'go to shop menu'
    quit_the_game: str = 'quit the game'


@dataclass
class Settings:
    screen_size_x: int = 1400
    screen_size_y: int = 900
    screen_size: Tuple[int, int] = screen_size_x, screen_size_y
    screen_center: Tuple[int, int] = screen_size_x // 2, screen_size_y // 2
    asteroids_start_amount: int = 1


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
