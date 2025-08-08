from pygame import Surface
from pygame.math import Vector2

from settings import Settings


class GameObject:
    def __init__(self, x: float, y: float) -> None:
        self.time_now: float = 0.0
        self.position: Vector2 = Vector2(x, y)
        self.velocity: Vector2 = Vector2(0, 0)
        self.angle = 0
        self.radius = 20
        self.alive = True

    def update(self, dt: float, time_now: float) -> None:
        self.time_now = time_now
        self.position += self.velocity * dt

        if self.position.x < 0:
            self.position.x = Settings.screen_size_x
        elif self.position.x > Settings.screen_size_x:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = Settings.screen_size_y
        elif self.position.y > Settings.screen_size_y:
            self.position.y = 0

    def draw(self, screen: Surface) -> None:
        pass

    def check_collision(self, other: 'GameObject') -> bool:
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)
