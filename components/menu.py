from typing import Callable

from pygame import (
    K_DOWN,
    K_KP_ENTER,
    K_RETURN,
    K_UP,
    Rect,
    Surface,
)
from pygame.draw import rect
from pygame.font import SysFont

from abstractions.apps import AppComponent
from settings import (
    AppEvents,
    Colors,
    Prices,
    Settings,
    UserStats,
)


class MenuItem:
    def __init__(self, text: str, action: Callable) -> None:
        self.text: str = text
        self.action: Callable = action


class BaseMenu(AppComponent):
    def __init__(self, screen: Surface) -> None:
        self.screen: Surface = screen
        self.event: AppEvents = AppEvents.no_event
        self.time_now: float = 0.0

        self.menu_title: str = ''

        self.font = SysFont('Arial', 24)
        self.font_title = SysFont('Arial', 62, True)
        self.font_small = SysFont('Arial', 18)

        self.menu_vertical_shift = 0
        self.menu_items: tuple[MenuItem, ...] = ()
        self.menu_item_height: int = 60
        self.menu_item_width: int = 400
        self.menu_items_gap: int = self.menu_item_height // 2
        self.menu_items_padding: int = self.menu_item_height // 3

        self.is_draw_stats: bool = False
        self.is_draw_help: bool = False
        self.selected_menu_item: int = 0

    def select_next_menu_item(self) -> None:
        if self.selected_menu_item == 0:
            self.selected_menu_item = len(self.menu_items)-1
        else:
            self.selected_menu_item -= 1

    def select_prev_menu_item(self) -> None:
        if self.selected_menu_item == len(self.menu_items)-1:
            self.selected_menu_item = 0
        else:
            self.selected_menu_item += 1

    def handle_input(self, inputs: set[int]) -> None:
        if (
            K_RETURN in inputs
            or K_KP_ENTER in inputs
        ):
            self.menu_items[self.selected_menu_item].action()

        if K_UP in inputs:
            self.select_next_menu_item()
        elif K_DOWN in inputs:
            self.select_prev_menu_item()

    def draw_stats(self) -> None:
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
            f'Bullets: {UserStats.max_bullets}',
            True,
            Colors.white,
        )
        self.screen.blit(level_text, (10, 10))
        self.screen.blit(score_text, (10, 40))
        self.screen.blit(lives_text, (10, 70))
        self.screen.blit(bullets_text, (10, 100))

    def draw_help(self) -> None:
        x0 = Settings.screen_center[0] - 300
        y0 = Settings.screen_center[1] - 200

        help_rect = Rect(
                x0,
                y0,
                600,
                400,
            )
        rect(
            self.screen,
            Colors.blue_dark,
            help_rect,
        )
        help_text = (
            'Shoot asteroids, yearn credits, buy upgrades.\n'
             '\n'
             '"Left arrow" and "Right arrow" to rotate the ship. \n'
             '"Up arrow" to accelerate.\n'
             '"Space" to shoot.\n'
             '"R" to reload.\n'
             '"ESC" to pause the game\n'
             '\n'
             'Have fun!'
             '\n\n\n\n'
             'Press "Enter" to close this window.'
        )
        lines = help_text.split('\n')
        y_offset = 0
        for line in lines:
            help_text = self.font_small.render(
                line,
                True,
                Colors.gray,
            )
            help_rect = help_text.get_rect(center=(
                Settings.screen_center[0],
                y0+50+y_offset,
            ))
            self.screen.blit(help_text, help_rect)
            y_offset += int(self.font_small.get_height() * 1.2)

    def draw_title(self) -> None:
        title_text = self.font_title.render(
            self.menu_title,
            True,
            Colors.green_acidic,
        )
        title_rect = title_text.get_rect(center=(
            Settings.screen_center[0],
            120,
        ))
        self.screen.blit(title_text, title_rect)

    def draw_menu(self) -> None:
        height: int = (
            self.menu_item_height * len(self.menu_items)
            + self.menu_items_gap * (len(self.menu_items)+1)
        )
        width: int = (
            self.menu_item_width + self.menu_items_gap*2
        )
        x0 = Settings.screen_center[0] - width // 2
        y0 = (
            Settings.screen_center[1]
            + self.menu_vertical_shift
            - height // 2
        )
        rect(
            self.screen,
            Colors.blue_dark,
            Rect(x0, y0, width, height),
        )
        for i in range(len(self.menu_items)):

            if i == self.selected_menu_item:
                color = Colors.green_dark
            else:
                color = Colors.blue

            menu_item_rect = Rect(
                x0+self.menu_items_padding,
                (
                    y0
                    + self.menu_items_gap
                    + (i*self.menu_items_gap)
                    + (i*self.menu_item_height)
                ),
                width-(self.menu_items_padding*2),
                self.menu_item_height,
            )
            text = self.font.render(
                self.menu_items[i].text,
                True,
                Colors.gray,
            )
            text_rect = text.get_rect(center=menu_item_rect.center)
            rect(
                self.screen,
                color,
                menu_item_rect,
            )
            self.screen.blit(text, text_rect)

    def draw_help_text(self) -> None:
        help_text = self.font_small.render(
            'Press "UP" or "DOWN" to select, "ENTER" to activate',
            True,
            Colors.gray,
        )
        help_rect = help_text.get_rect(
            center=(
                Settings.screen_center[0],
                Settings.screen_size_y-50,
            ),
        )
        self.screen.blit(help_text, help_rect)

    def draw(self) -> None:
        self.screen.fill(Colors.blue_darker)
        self.draw_title()
        self.draw_menu()
        self.draw_help_text()

        if self.is_draw_stats:
            self.draw_stats()

        if self.is_draw_help:
            self.draw_help()

    def update(self, dt: float, time_now: float) -> None:
        self.time_now = time_now


class MainMenu(BaseMenu):
    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)
        self.menu_title = 'Space Miner'
        self.menu_items = (
            MenuItem('Start new game', self.go_to_game),
            MenuItem('How to play', self.show_how_to_play),
            MenuItem('Quit', self.quit_app),
        )

    def go_to_game(self) -> None:
        self.event = AppEvents.go_to_the_game

    def show_how_to_play(self) -> None:
        if self.is_draw_help:
            self.is_draw_help = False
        else:
            self.is_draw_help = True

    def quit_app(self) -> None:
        self.event = AppEvents.quit_the_game


class PauseMenu(MainMenu):
    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)
        self.menu_items[0].text = 'Resume your game'
        self.is_draw_stats = True


class ShopMenu(BaseMenu):
    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)
        self.menu_title = 'Shop'
        self.menu_item_width = 500
        self.menu_items = (
            MenuItem(
                f'Buy gun upgrade ({Prices.bullets} cr.)',
                self.increase_max_bullets,
            ),
            MenuItem(
                f'Buy additional live ({Prices.lives} cr.)',
                self.increase_lives,
            ),
            MenuItem(
                'Start next level',
                self.go_to_next_level,
            ),
        )
        self.is_draw_stats = True

    @staticmethod
    def is_enough_credits(cost: int) -> bool:
        return UserStats.credits - cost >= 0

    def increase_max_bullets(self) -> None:
        if self.is_enough_credits(Prices.bullets):
            UserStats.credits -= Prices.bullets
            UserStats.max_bullets += 5

    def increase_lives(self) -> None:
        if self.is_enough_credits(Prices.lives):
            UserStats.credits -= Prices.lives
            UserStats.lives += 1

    def go_to_next_level(self) -> None:
        UserStats.level += 1
        self.event = AppEvents.go_to_the_game

    def show_how_to_play(self) -> None:
        pass

    def quit_app(self) -> None:
        self.event = AppEvents.quit_the_game
