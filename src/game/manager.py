import pygame
from states.main_menu import MainMenuState
# + импорт других состояний: PlayState, LoadState...

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.states = {}
        self.current_state = None

        # Регистрируем состояния
        self.register_state("menu", MainMenuState(self))
        # self.register_state("play", PlayState(self))
        # self.register_state("load", LoadState(self))

        # Сразу показываем меню
        self.change_state("menu")

    def register_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        self.current_state = self.states[name]

    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def render(self):
        if self.current_state:
            self.current_state.render(self.screen)

    def quit(self):
        self.running = False
