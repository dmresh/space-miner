
from abc import ABC, abstractmethod
from typing import Set

import pygame as pg


class AppComponent(ABC):
    @abstractmethod
    def __init__(self, screen: pg.Surface) -> None:
        self.screen: pg.Surface
        self.event: str
        self.time_now: float

    @abstractmethod
    def handle_input(self, inputs: Set[int]) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self, dt: float, time_now: float) -> None:
        pass
