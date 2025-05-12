from src.game.state_manager import StateManager
from src.states.briefing_state import BriefingState
from src.states.main_menu_state import MainMenuState
from src.states.pause_state import PauseState
from src.states.play_state import PlayState


def register_states(manager: StateManager) -> None:
    manager.register_state("menu", MainMenuState)
    manager.register_state("briefing", BriefingState)
    manager.register_state("play", PlayState)
    manager.register_state("pause", PauseState)
