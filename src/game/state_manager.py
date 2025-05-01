import pygame

from typing import Dict, Optional

from src.states.base_state import BaseState

# + импорт других состояний: PlayState, LoadState...

class StateManager:
    def __init__(self):
        self._states: Dict[str, BaseState] = {}
        self._current_state: Optional[BaseState] = None
        self.quit: bool = False

    @property
    def current_state(self) -> BaseState:
        return self._current_state

    def register_state(self, name: str, state: BaseState) -> None:
        self._states[name] = state

    def change_state(self, name: str) -> None:
        if name in self._states:
            self._current_state = self._states[name]
        else:
            # Можно залогировать или пробросить своё исключение
            print(f"Warning: state '{name}' is not registered.")
