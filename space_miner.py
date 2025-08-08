from time import time
from typing import TYPE_CHECKING

import pygame as pg
from pygame import Surface
from pygame.time import Clock

from components.game import Game
from components.menu import (
    MainMenu,
    PauseMenu,
    ShopMenu,
)
from settings import AppEvents, Settings

if TYPE_CHECKING:
    from abstractions.apps import AppComponent


class Main:
    def __init__(self) -> None:
        pg.display.set_caption('Space Miner')
        self.screen: Surface = pg.display.set_mode(Settings.screen_size)
        self.clock: Clock = Clock()

        self.main_menu: AppComponent = MainMenu(self.screen)
        self.game: AppComponent = Game(self.screen)
        self.pause: AppComponent = PauseMenu(self.screen)
        self.shop: AppComponent = ShopMenu(self.screen)

        self.current_component: AppComponent = self.main_menu
        self.is_running: bool = True

    def handle_input(self) -> set[int]:
        keys_pressed: set[int] = set()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
                break

            if event.type == pg.KEYDOWN:
                keys_pressed.add(event.key)

        return keys_pressed

    def run(self) -> None:
        while self.is_running:

            dt = self.clock.tick(60) / 1000.0

            self.current_component.handle_input(self.handle_input())
            self.current_component.update(dt, time())
            self.current_component.draw()

            pg.display.flip()

            event = self.current_component.event
            self.current_component.event = AppEvents.no_event
            match event:
                case AppEvents.quit_the_game:
                    self.is_running = False
                    break
                case AppEvents.go_to_main_menu:
                    self.current_component = self.main_menu
                case AppEvents.go_to_the_game:
                    self.current_component = self.game
                case AppEvents.go_to_pause_menu:
                    self.current_component = self.pause
                case AppEvents.go_to_shop_menu:
                    self.current_component = self.shop

        pg.quit()


if __name__ == '__main__':
    pg.init()
    Main().run()
