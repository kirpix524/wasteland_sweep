import pygame

from typing import Dict, Optional, Callable

from src.game.game_session import GameSession
from src.states.base_state import BaseState

# + импорт других состояний: PlayState, LoadState...

class StateManager:
    def __init__(self, game_session: GameSession):
        self._states: Dict[str, type[BaseState]] = {}
        self._game_session = game_session
        self._current_state: Optional[BaseState] = None
        self.quit: bool = False

    @property
    def current_state(self) -> BaseState:
        return self._current_state

    @property
    def game_session(self) -> GameSession:
        return self._game_session

    def register_state(self, name: str, state: type[BaseState]) -> None:
        self._states[name] = state

    def change_state(self, name: str, **kwargs) -> None:
        if name in self._states:
            state_class = self._states[name]
            new_state = state_class(self, **kwargs) #'BaseState' object is not callable
            self._current_state = new_state
        else:
            # Можно залогировать или пробросить своё исключение
            print(f"Warning: state '{name}' is not registered.")
