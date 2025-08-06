from random import randint
from typing import List, Set, Tuple

import pygame as pg

from abstractions.apps import AppComponent
from components.game_objects.asteroid import Asteroid
from components.game_objects.ship import Ship
from settings import (
    DefaultStats,
    Colors,
    Settings,
    UserStats,
)
from settings import AppEvents


class Game(AppComponent):
    def __init__(self, screen: pg.Surface) -> None:
        self.event: str = ''
        self.time_now: float = 0.0

        self.screen = screen
        self.screen_center: Tuple[int, int] = Settings.screen_center
        self.font = pg.font.SysFont("Arial", 24)
        self.asteroids: List[Asteroid] = []
        self.asteroids_amount: int = Settings.asteroids_start_amount

        self.current_level = UserStats.level
        self.game_over = False

        self.restart()
        self.generate_ship()
        self.generate_asteroids()

    def generate_ship(self) -> None:
        self.ship = Ship(*Settings.screen_center)
        self.ship.velocity = pg.math.Vector2(0, 0)
        self.ship_spawned_at: float = self.time_now

    def is_place_far_for_ship(self, x: int, y: int) -> bool:
        place: pg.Vector2 = pg.math.Vector2(x, y)
        if (place.distance_to(self.ship.position) > 100):
            return True
        return False

    def generate_asteroids(self):
        "Generationg asteroids."
        while len(self.asteroids) <= self.asteroids_amount:
            x = randint(0, Settings.screen_size_x)
            y = randint(0, Settings.screen_size_y)

            if self.is_place_far_for_ship(x, y):
                self.asteroids.append(Asteroid(x, y))

    def go_to_main_menu(self):
        self.event = AppEvents.go_to_main_menu

    def go_to_pause_menu(self):
        self.event = AppEvents.go_to_pause_menu

    def go_to_shop_menu(self):
        self.event = AppEvents.go_to_shop_menu

    def handle_input(self, inputs: Set[int]) -> None:
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.ship.rotation_speed = -180
        elif keys[pg.K_RIGHT]:
            self.ship.rotation_speed = 180
        else:
            self.ship.rotation_speed = 0

        if keys[pg.K_UP]:
            self.ship.thrust = 200
        else:
            self.ship.thrust = 0

        if keys[pg.K_SPACE]:
            self.ship.shoot()

        if pg.K_r in inputs:
            self.ship.start_reloading()

        if pg.K_ESCAPE in inputs:
            self.go_to_pause_menu()

    def check_collisions_bullets_and_asteroids(self):
        "Проверка столкновений пуль с астероидами."
        for bullet in self.ship.bullets[:]:
            for asteroid in self.asteroids[:]:
                if bullet.check_collision(asteroid):
                    self.ship.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)

                    UserStats.credits += (4 - asteroid.size) * 100

                    fragments = asteroid.split()
                    self.asteroids.extend(fragments)
                    break

    def check_collisions_ship_and_asteroids(self):
        "Проверка столкновений корабля с астероидами."
        for asteroid in self.asteroids[:]:
            if (
                self.ship.check_collision(asteroid)
                and self.time_now > self.ship_spawned_at + 2.0
            ):
                self.generate_ship()
                UserStats.lives -= 1

            if UserStats.lives < 1:
                self.game_over = True

    def check_for_win(self):
        "Проверка победы (все астероиды уничтожены)."
        if not self.asteroids:
            self.go_to_shop_menu()

    def start_new_level(self):
        "Создание нового уровня."
        self.current_level = UserStats.level

        self.generate_ship()
        self.ship.cur_bullets = UserStats.max_bullets

        self.asteroids_amount = 3 * UserStats.level
        self.generate_asteroids()

    def update(self, dt, time_now: float):
        self.time_now = time_now

        if self.game_over:
            self.restart()
            self.go_to_main_menu()
            return

        if self.current_level != UserStats.level:
            self.start_new_level()

        self.ship.update(dt, time_now)

        for asteroid in self.asteroids:
            asteroid.update(dt, time_now)

        self.check_collisions_bullets_and_asteroids()
        self.check_collisions_ship_and_asteroids()
        self.check_for_win()

    def draw(self):
        self.screen.fill(Colors.blue_darker)

        if not self.game_over:
            self.ship.draw(self.screen)

            for asteroid in self.asteroids:
                asteroid.draw(self.screen)

        level_text = self.font.render(
            f"Level: {UserStats.level}",
            True,
            Colors.white,
        )
        score_text = self.font.render(
            f"Credits: {UserStats.credits}",
            True,
            Colors.white,
        )
        lives_text = self.font.render(
            f"Lives: {UserStats.lives}",
            True,
            Colors.white,
        )
        bullets_text = self.font.render(
            f"Bullets: [{self.ship.cur_bullets} / {UserStats.max_bullets}] "
            + ("|" * self.ship.cur_bullets),
            True,
            Colors.white,
        )
        bullets_text_reloading = self.font.render(
            "Bullets: RELOADING...",
            True,
            Colors.red,
        )

        self.screen.blit(level_text, (10, 10))
        self.screen.blit(score_text, (10, 40))
        self.screen.blit(lives_text, (10, 70))

        if not self.ship.is_reloading:
            self.screen.blit(
                bullets_text,
                (10, Settings.screen_size_y - 50)
            )
        else:
            self.screen.blit(
                bullets_text_reloading,
                (10, Settings.screen_size_y - 50)
            )


    def restart(self):
        UserStats.credits = DefaultStats.credits
        UserStats.lives = DefaultStats.lives
        UserStats.level = DefaultStats.level
        UserStats.max_bullets = DefaultStats.max_bullets

        self.asteroids = []
        self.asteroids_amount = Settings.asteroids_start_amount
        self.game_over = False

        self.generate_ship()
        self.generate_asteroids()
