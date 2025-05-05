import pygame
from typing import TYPE_CHECKING

from src.states.base_state import BaseState
from src.settings import BRIEFING_BG_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT

if TYPE_CHECKING:
    from src.game.state_manager import StateManager
    from src.game.game_session import GameSession

class BriefingState(BaseState):
    def __init__(self, manager: 'StateManager', message: str) -> None:
        super().__init__(manager)
        # Текст брифинга перед уровнем
        self._message: str = message
        # Загрузка и масштабирование фона
        bg: pygame.Surface = pygame.image.load(BRIEFING_BG_IMAGE).convert()
        self._background: pygame.Surface = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Опции меню
        self._options: list[str] = ["Продолжить", "Назад"]
        self._selected_index: int = 0
        # Шрифт для текста
        self._font: pygame.font.Font = pygame.font.Font(None, 36)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._selected_index = (self._selected_index - 1) % len(self._options)
            elif event.key == pygame.K_DOWN:
                self._selected_index = (self._selected_index + 1) % len(self._options)
            elif event.key == pygame.K_RETURN:
                choice: str = self._options[self._selected_index]
                if choice == "Продолжить":
                    self.manager.change_state("play", game_session=self.manager.game_session)
                else:
                    self.manager.change_state("menu")

    def update(self, dt: float) -> None:
        # Логика не требуется для статичного экрана брифинга
        pass

    def render(self, surface: pygame.Surface) -> None:
        # Отрисовка фона
        surface.blit(self._background, (0, 0))

        # Отрисовка текста брифинга по центру сверху
        lines: list[str] = self._message.split("\n")
        for i, line in enumerate(lines):
            text_surf: pygame.Surface = self._font.render(line, True, (255, 255, 255))
            rect: pygame.Rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
            surface.blit(text_surf, rect)

        # Отрисовка опций меню по центру экрана
        for i, option in enumerate(self._options):
            color: tuple[int, int, int] = (255, 255, 0) if i == self._selected_index else (255, 255, 255)
            text_surf: pygame.Surface = self._font.render(option, True, color)
            rect: pygame.Rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            surface.blit(text_surf, rect)
