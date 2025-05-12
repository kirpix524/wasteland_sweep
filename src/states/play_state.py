from itertools import count

import pygame
from typing import TYPE_CHECKING, Any

from src.states.base_state import BaseState
from src.game.input_handler import PlayStateInputHandler

if TYPE_CHECKING:
    from src.game.game_session import GameSession
    from src.game.state_manager import StateManager

class PlayState(BaseState):
    def __init__(self, state_manager: 'StateManager', game_session: 'GameSession') -> None:
        super().__init__(state_manager)
        self._game_session = game_session
        self._state_manager = state_manager

    @property
    def game_session(self) -> 'GameSession':
        return self._game_session

    def handle_event(self, event: Any) -> None:
        super().handle_event(event)
        PlayStateInputHandler.handle(event, self)

    def update(self, dt: float) -> None:
        super().update(dt)
        self._game_session.current_level.player_controller.update(dt)
        self._game_session.current_level.update(dt)


    def show_text(self, surface: 'pygame.Surface', text: str, font_size: int, x: int, y: int, color: tuple) -> None:
        font = pygame.font.Font(None, font_size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(topright=(x, y))
        surface.blit(text_surf, text_rect)

    def show_info(self, surface: 'pygame.Surface') -> None:
        from src.settings import SCREEN_WIDTH
        player = self._game_session.current_level.player_controller.player
        weapon = player.equipped_weapon
        current_ammo = weapon.current_ammo if weapon else 0
        weapon_name = weapon.name if weapon else "Отсутствует"
        fire_mode = weapon.current_fire_mode if weapon else ""
        entity_manager = self._game_session.current_level.entity_manager
        objects = len(entity_manager.all_entities)

        # Отображение названия оружия и оставшихся патронов в верхнем правом углу
        weapon_text = f"Оружие: {weapon_name} "
        fire_mode_text = f"Режим огня: {fire_mode}"
        ammo_text = f"Патроны: {current_ammo}"
        obj_text = f"Объектов: {objects}"
        cur_health_text = f"Здоровье: {player.health} / {player.max_health}"

        black_color = (0, 0, 0)
        self.show_text(surface, weapon_text, 34, SCREEN_WIDTH - 10, 10, black_color)
        self.show_text(surface, ammo_text, 34, SCREEN_WIDTH - 10, 40, black_color)
        self.show_text(surface, fire_mode_text, 34, SCREEN_WIDTH - 10, 70, black_color)
        self.show_text(surface, obj_text, 34, SCREEN_WIDTH - 10, 100, black_color)
        self.show_text(surface, cur_health_text, 34, SCREEN_WIDTH - 10, 130, black_color)

    def render(self, surface: 'pygame.Surface') -> None:
        super().render(surface)
        self._game_session.current_level.render(surface)
        self.show_info(surface)

