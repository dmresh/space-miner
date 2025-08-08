from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pygame import Surface

if TYPE_CHECKING:
    from settings import AppEvents


class AppComponent(ABC):
    @abstractmethod
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.screen: Surface
        self.event: AppEvents
        self.time_now: float

    @abstractmethod
    def handle_input(self, inputs: set[int]) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self, dt: float, time_now: float) -> None:
        pass
