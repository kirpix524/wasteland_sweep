import pygame
from typing import Any

from src.game.state_manager import StateManager
from src.settings import MENU_BG_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.states.base_state import BaseState

class WinState(BaseState):
    """
    Состояние победы: отображает сообщение о завершении уровня и возвращает игрока в главное меню.
    """
    def __init__(self, manager: StateManager, message: str = "Уровень пройден!") -> None:
        super().__init__(manager)
        self.__message: str = message
        self.__font: pygame.font.Font = pygame.font.SysFont(None, 72)
        bg = pygame.image.load(MENU_BG_IMAGE)
        # Подгоняем размер под экран
        self.__background: pygame.Surface = pygame.transform.scale(
            bg.convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    @property
    def message(self) -> str:
        """Сообщение, отображаемое на экране победы."""
        return self.__message

    def handle_event(self, event: pygame.event.Event) -> None:
        """Обрабатывает нажатие любой клавиши: возвращает в главное меню."""
        if event.type == pygame.KEYDOWN:
            # По любому нажатию возвращаемся в главное меню
            self.manager.change_state("menu")

    def update(self, dt: float) -> None:
        """Обновление не требуется для экрана победы."""
        pass

    def render(self, surface: Any) -> None:
        """Отрисовать фон и сообщение о победе по центру экрана."""
        surface.blit(self.__background, (0, 0))
        label = self.__font.render(self.__message, True, (0, 255, 0))
        x = surface.get_width() // 2 - label.get_width() // 2
        y = surface.get_height() // 2 - label.get_height() // 2
        surface.blit(label, (x, y))
