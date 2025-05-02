from typing import TYPE_CHECKING, Any

from src.game.level_manager import LevelManager
from src.states.base_state import BaseState
from src.game.input_handler import PlayStateInputHandler

if TYPE_CHECKING:
    from src.game.state_manager import StateManager
    import pygame

class PlayState(BaseState):
    def __init__(self, state_manager: 'StateManager', level_manager: 'LevelManager', level_number: int = 1) -> None:
        super().__init__(state_manager)
        self._level_number: int = level_number
        self._level_manager = level_manager
        self._level_manager.load_level(self._level_number)
        self._state_manager = state_manager

    @property
    def level_number(self) -> int:
        return self._level_number

    def handle_event(self, event: Any) -> None:
        super().handle_event(event)
        PlayStateInputHandler.handle(event, self._level_manager.current_level.player_controller)

    def update(self, dt: float) -> None:
        super().update(dt)
        self._level_manager.current_level.update(dt)

    def render(self, surface: 'pygame.Surface') -> None:
        super().render(surface)
        self._level_manager.current_level.render(surface)
