from src.game.state_manager import StateManager
from src.states.briefing_state import BriefingState
from src.states.lose_state import LoseState
from src.states.main_menu_state import MainMenuState
from src.states.pause_state import PauseState
from src.states.play_state import PlayState
from src.states.win_state import WinState


def register_states(manager: StateManager) -> None:
    manager.register_state("menu", MainMenuState)
    manager.register_state("briefing", BriefingState)
    manager.register_state("play", PlayState)
    manager.register_state("pause", PauseState)
    manager.register_state("win", WinState)
    manager.register_state("lose", LoseState)
