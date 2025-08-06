from pygame.draw import circle

from components.game_objects.game_object import GameObject
from settings import (
    Settings,
    Colors,
)


class Bullet(GameObject):
    def __init__(self, x, y, velocity) -> None:
        super().__init__(x, y)
        self.time_now: float = 0.0
        self.velocity = velocity
        self.radius: int = 2

    def update(self, dt, time_now: float):
        self.time_now = time_now
        self.position += self.velocity * dt

        if self.position.x < 0 or self.position.x > Settings.screen_size_x:
            self.alive = False

        if self.position.y < 0 or self.position.y > Settings.screen_size_y:
            self.alive = False

    def draw(self, screen):
        circle(
            screen,
            Colors.yellow,
            (int(self.position.x), int(self.position.y)),
            self.radius,
        )
