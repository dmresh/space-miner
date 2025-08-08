from pygame import Surface
from pygame.draw import polygon
from pygame.math import Vector2

from components.game_objects.bullet import Bullet
from components.game_objects.game_object import GameObject
from settings import (
    DefaultStats,
    UserStats,
)


class Ship(GameObject):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.time_now: float = 0.0
        self.radius: float = 10.0
        self.thrust: float = 0.0
        self.rotation_speed: float = 0.0
        self.bullets: list[Bullet] = []
        self.cur_bullets = DefaultStats.max_bullets
        self.last_shot_time: float = 0.0
        self.last_reload_time: float = 0.0
        self.is_reloading: bool = False

    def update(self, dt: float, time_now: float) -> None:
        self.time_now = time_now
        self.angle += self.rotation_speed * dt

        if self.thrust > 0:
            thrust_vector = Vector2(0, -self.thrust)
            thrust_vector.rotate_ip(self.angle)
            self.velocity += thrust_vector * dt

        self.velocity *= 0.99

        super().update(dt, self.time_now)

        for bullet in self.bullets[:]:
            bullet.update(dt, self.time_now)
            if not bullet.alive:
                self.bullets.remove(bullet)

        if (
            self.is_reloading
            and self.time_now > self.last_reload_time + 3.0
        ):
            self.end_reloading()

    def can_shoot(self) -> bool:
        if (
            self.time_now > self.last_shot_time + 0.1
            and self.cur_bullets > 0
            and not self.is_reloading
        ):
            self.last_shot_time = self.time_now
            return True
        return False

    def shoot(self) -> None:
        if self.can_shoot():
            bullet_velocity = Vector2(0, -300)
            bullet_velocity.rotate_ip(self.angle)
            bullet_velocity += self.velocity

            bullet = Bullet(self.position.x, self.position.y, bullet_velocity)
            self.bullets.append(bullet)
            self.cur_bullets -= 1

    def start_reloading(self) -> None:
        if not self.is_reloading:
            self.last_reload_time = self.time_now
            self.is_reloading = True

    def end_reloading(self) -> None:
        self.cur_bullets = UserStats.max_bullets
        self.is_reloading = False

    def draw(self, screen: Surface) -> None:
        points = [
            Vector2(0, -self.radius),
            Vector2(-self.radius//2, self.radius),
            Vector2(self.radius//2, self.radius),
        ]

        rotated_points = []
        for point in points:
            point.rotate_ip(self.angle)
            rotated_points.append(point + self.position)

        polygon(screen, (255, 255, 255), rotated_points)

        for bullet in self.bullets:
            bullet.draw(screen)
