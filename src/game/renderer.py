import pygame

from src.states.base_state import BaseState

class Renderer:
    @staticmethod
    def render(screen: pygame.Surface, state: BaseState) -> None:
        state.render(screen)
        # сюда можно добавить стек слоёв, пост-эффекты и т.п.
