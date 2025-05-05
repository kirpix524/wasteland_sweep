from typing import TYPE_CHECKING, Any


from src.game.level_manager import LevelManager
from src.states.base_state import BaseState
from src.game.input_handler import PlayStateInputHandler

if TYPE_CHECKING:
    from src.game.game_session import GameSession
    from src.game.state_manager import StateManager
    import pygame

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
        PlayStateInputHandler.handle(event, self._game_session.current_level.player_controller)

    def update(self, dt: float) -> None:
        super().update(dt)
        self._game_session.current_level.update(dt)

    def render(self, surface: 'pygame.Surface') -> None:
        super().render(surface)
        self._game_session.current_level.render(surface)
