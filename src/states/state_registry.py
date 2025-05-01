from src.game.state_manager import StateManager
from src.states.main_menu import MainMenuState

def register_states(manager: StateManager) -> None:
    manager.register_state("menu", MainMenuState(manager))
    # manager.register_state("play", PlayState(manager))
    # manager.register_state("load", LoadState(manager))
