import pygame

from src.states.base_state import BaseState

class InputHandler:
    @staticmethod
    def handle(event: pygame.event.Event, state: BaseState) -> None:
        # Преобразуем кнопку в команду, либо сразу передаём
        state.handle_event(event)
