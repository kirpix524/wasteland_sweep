import pygame

from src.game.input_handler import MainMenuStateInputHandler
from src.states.base_state import BaseState
from src.game.state_manager import StateManager

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BG_IMAGE

class MainMenuState(BaseState):
    OPTIONS = ["New Game", "Load Game", "Exit"]

    def __init__(self, manager: StateManager):
        super().__init__(manager)
        self.__selected = 0
        self.__font = pygame.font.SysFont(None, 58)
        bg = pygame.image.load(MENU_BG_IMAGE)
        # Подгоняем размер под экран
        self.__background = pygame.transform.scale(bg.convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def change_selected(self, delta):
        self.__selected = (self.__selected + delta) % len(self.OPTIONS)

    def get_selected(self):
        choice = self.OPTIONS[self.__selected]
        if choice == "New Game":
            self.manager.change_state("play")  # или конкретный PlayState
        elif choice == "Load Game":
            self.manager.change_state("load")  # State для загрузки
        else:
            self.manager.quit = True

    def handle_event(self, event):
        MainMenuStateInputHandler.handle(event, self)

    def update(self, dt):
        pass

    def render(self, surface):
        surface.blit(self.__background, (0, 0))
        for i, text in enumerate(self.OPTIONS):
            color = (255,255,0) if i == self.__selected else (200, 200, 200)
            label = self.__font.render(text, True, color)
            x = surface.get_width() // 2 - label.get_width() // 2
            y = surface.get_height() // 2 + i * 60
            surface.blit(label, (x, y))
