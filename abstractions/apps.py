from abc import ABC, abstractmethod

from pygame import Surface


class AppComponent(ABC):
    @abstractmethod
    def __init__(self, screen: Surface) -> None:
        self.screen: Surface
        self.event: str
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
