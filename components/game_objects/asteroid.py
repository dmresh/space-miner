import random

from pygame import Surface
from pygame.draw import polygon
from pygame.math import Vector2

from components.game_objects.game_object import GameObject


class Asteroid(GameObject):
    def __init__(self, x: float, y: float, size: int =3) -> None:
        super().__init__(x, y)
        self.time_now: float = 0.0
        self.size = size
        self.radius = size * 10
        self.rotation_speed = random.uniform(-180, 180)

        speed = random.uniform(50, 150)
        angle = random.uniform(0, 360)
        self.velocity = Vector2(speed, 0)
        self.velocity.rotate_ip(angle)

        self.vertices = []
        num_vertices = 8
        for i in range(num_vertices):
            angle = (360 / num_vertices) * i
            radius_variation = random.uniform(0.8, 1.2)
            vertex_radius = self.radius * radius_variation
            vertex = Vector2(vertex_radius, 0)
            vertex.rotate_ip(angle)
            self.vertices.append(vertex)

    def update(self, dt: float, time_now: float) -> None:
        self.time_now = time_now
        super().update(dt, time_now)
        self.angle += self.rotation_speed * dt

    def draw(self, screen: Surface) -> None:
        rotated_vertices = []
        for vertex in self.vertices:
            rotated_vertex = vertex.copy()
            rotated_vertex.rotate_ip(self.angle)
            rotated_vertex += self.position
            rotated_vertices.append(rotated_vertex)

        polygon(screen, (100, 100, 100), rotated_vertices, 2)

    def split(self) -> 'list[Asteroid]':
        if self.size > 1:
            fragments = []
            for _ in range(2):
                fragment = Asteroid(
                    self.position.x,
                    self.position.y,
                    self.size - 1,
                )
                fragment.velocity += Vector2(
                    random.uniform(-100, 100),
                    random.uniform(-100, 100),
                )
                fragments.append(fragment)
            return fragments
        return []
