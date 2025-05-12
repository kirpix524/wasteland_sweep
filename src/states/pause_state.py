from typing import TYPE_CHECKING
import pygame

from src.states.base_state import BaseState
from src.settings import MENU_BG_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.game.input_handler import PauseStateInputHandler

if TYPE_CHECKING:
    from src.game.state_manager import StateManager

class PauseState(BaseState):
    #OPTIONS = ["Вернуться в игру", "Сохранить игру", "Выйти в главное меню"]
    OPTIONS = ["Вернуться в игру", "Выйти в главное меню"]

    def __init__(self, manager: 'StateManager') -> None:
        super().__init__(manager)
        self.__selected: int = 0
        self.__font: pygame.font.Font = pygame.font.SysFont(None, 58)
        bg = pygame.image.load(MENU_BG_IMAGE)
        # Подгоняем размер под экран
        self.__background: pygame.Surface = pygame.transform.scale(
            bg.convert_alpha(),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    def change_selected(self, delta: int) -> None:
        self.__selected = (self.__selected + delta) % len(self.OPTIONS)

    def get_selected(self) -> None:
        choice: str = self.OPTIONS[self.__selected]
        if choice == "Вернуться в игру":
            # Возвращаемся к игровому состоянию (PlayState)
            self.manager.change_state("play", game_session=self.manager.game_session)
        elif choice == "Сохранить игру":
            # Сохраняем текущую сессию
            self.manager.game_session.save()
            # Остаёмся в меню паузы
        else:  # "Выйти в главное меню"
            self.manager.change_state("menu")

    def handle_event(self, event: pygame.event.Event) -> None:
        PauseStateInputHandler.handle(event, self)

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.__background, (0, 0))
        for i, text in enumerate(self.OPTIONS):
            color = (255, 255, 0) if i == self.__selected else (200, 200, 200)
            label = self.__font.render(text, True, color)
            x = surface.get_width() // 2 - label.get_width() // 2
            y = surface.get_height() // 2 + i * 60
            surface.blit(label, (x, y))


