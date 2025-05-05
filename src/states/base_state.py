from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.state_manager import StateManager


class BaseState:
    def __init__(self, manager: 'StateManager', **kwargs):
        self.manager:'StateManager' = manager


    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        pass
