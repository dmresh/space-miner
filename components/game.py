from random import randint

from pygame import (
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_UP,
    K_r,
    Surface,
)
from pygame.font import SysFont
from pygame.key import get_pressed
from pygame.math import Vector2

from abstractions.apps import AppComponent
from components.game_objects.asteroid import Asteroid
from components.game_objects.ship import Ship
from settings import (
    AppEvents,
    Colors,
    DefaultStats,
    Settings,
    UserStats,
)


class Game(AppComponent):
    def __init__(self, screen: Surface) -> None:
        self.event: AppEvents = AppEvents.no_event
        self.time_now: float = 0.0

        self.screen = screen
        self.screen_center: tuple[int, int] = Settings.screen_center
        self.font = SysFont('Arial', 24)
        self.asteroids: list[Asteroid] = []
        self.asteroids_amount: int = Settings.asteroids_start_amount

        self.current_level: int = UserStats.level
        self.ship: Ship = Ship(*Settings.screen_center)
        self.ship_spawned_at: float = self.time_now
        self.game_over: bool = False

        self.restart()
        self.generate_ship()
        self.generate_asteroids()

    def generate_ship(self) -> None:
        self.ship = Ship(*Settings.screen_center)
        self.ship.velocity = Vector2(0, 0)
        self.ship_spawned_at = self.time_now

    def is_place_far_for_ship(self, x: int, y: int) -> bool:
        place: Vector2 = Vector2(x, y)
        return place.distance_to(self.ship.position) > Settings.safe_distance

    def generate_asteroids(self) -> None:
        while len(self.asteroids) < self.asteroids_amount:
            x = randint(0, Settings.screen_size_x)
            y = randint(0, Settings.screen_size_y)

            if self.is_place_far_for_ship(x, y):
                self.asteroids.append(Asteroid(x, y))

    def go_to_main_menu(self) -> None:
        self.event = AppEvents.go_to_main_menu

    def go_to_pause_menu(self) -> None:
        self.event = AppEvents.go_to_pause_menu

    def go_to_shop_menu(self) -> None:
        self.event = AppEvents.go_to_shop_menu

    def handle_input(self, inputs: set[int]) -> None:
        keys = get_pressed()

        if keys[K_LEFT]:
            self.ship.rotation_speed = -180
        elif keys[K_RIGHT]:
            self.ship.rotation_speed = 180
        else:
            self.ship.rotation_speed = 0

        if keys[K_UP]:
            self.ship.thrust = 200
        else:
            self.ship.thrust = 0

        if keys[K_SPACE]:
            self.ship.shoot()

        if K_r in inputs:
            self.ship.start_reloading()

        if K_ESCAPE in inputs:
            self.go_to_pause_menu()

    def check_collisions_bullets_and_asteroids(self) -> None:
        for bullet in self.ship.bullets[:]:
            for asteroid in self.asteroids[:]:
                if bullet.check_collision(asteroid):
                    self.ship.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)

                    UserStats.credits += (4 - asteroid.size) * 100

                    fragments = asteroid.split()
                    self.asteroids.extend(fragments)
                    break

    def check_collisions_ship_and_asteroids(self) -> None:
        for asteroid in self.asteroids[:]:
            if (
                self.ship.check_collision(asteroid)
                and self.time_now > self.ship_spawned_at + 2.0
            ):
                self.generate_ship()
                UserStats.lives -= 1

            if UserStats.lives < 1:
                self.game_over = True

    def check_for_win(self) -> None:
        if not self.asteroids:
            self.go_to_shop_menu()

    def start_new_level(self) -> None:
        self.current_level = UserStats.level

        self.generate_ship()
        self.ship.cur_bullets = UserStats.max_bullets

        self.asteroids_amount = 2 * UserStats.level
        self.generate_asteroids()

    def update(self, dt: float, time_now: float) -> None:
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

    def draw(self) -> None:
        self.screen.fill(Colors.blue_darker)

        if not self.game_over:
            self.ship.draw(self.screen)

            for asteroid in self.asteroids:
                asteroid.draw(self.screen)

        level_text = self.font.render(
            f'Level: {UserStats.level}',
            True,
            Colors.white,
        )
        score_text = self.font.render(
            f'Credits: {UserStats.credits}',
            True,
            Colors.white,
        )
        lives_text = self.font.render(
            f'Lives: {UserStats.lives}',
            True,
            Colors.white,
        )
        bullets_text = self.font.render(
            f'Bullets: [{self.ship.cur_bullets} / {UserStats.max_bullets}] '
            + ('|' * self.ship.cur_bullets),
            True,
            Colors.white,
        )
        bullets_text_reloading = self.font.render(
            'Bullets: RELOADING...',
            True,
            Colors.red,
        )

        self.screen.blit(level_text, (10, 10))
        self.screen.blit(score_text, (10, 40))
        self.screen.blit(lives_text, (10, 70))

        if not self.ship.is_reloading:
            self.screen.blit(
                bullets_text,
                (10, Settings.screen_size_y - 50),
            )
        else:
            self.screen.blit(
                bullets_text_reloading,
                (10, Settings.screen_size_y - 50),
            )


    def restart(self) -> None:
        UserStats.credits = DefaultStats.credits
        UserStats.lives = DefaultStats.lives
        UserStats.level = DefaultStats.level
        UserStats.max_bullets = DefaultStats.max_bullets

        self.asteroids.clear()
        self.asteroids_amount = Settings.asteroids_start_amount
        self.game_over = False

        self.generate_ship()
        self.generate_asteroids()
