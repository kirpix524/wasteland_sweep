import pygame
import os
from .base_state import BaseState

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BG_IMAGE

class MainMenuState(BaseState):
    OPTIONS = ["New Game", "Load Game", "Exit"]

    def __init__(self, manager):
        super().__init__(manager)
        self.selected = 0
        self.font = pygame.font.SysFont(None, 48)
        # Загрузка фона
        print("Loading menu background from:", MENU_BG_IMAGE,
              "→ exists?", os.path.exists(MENU_BG_IMAGE))
        bg = pygame.image.load(MENU_BG_IMAGE)
        # Подгоняем размер под экран
        self.background = pygame.transform.scale(bg.convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                choice = self.OPTIONS[self.selected]
                if choice == "New Game":
                    self.manager.change_state("play")    # или конкретный PlayState
                elif choice == "Load Game":
                    self.manager.change_state("load")    # State для загрузки
                else:
                    self.manager.quit()

    def update(self, dt):
        pass

    def render(self, surface):
        surface.blit(self.background, (0, 0))
        for i, text in enumerate(self.OPTIONS):
            color = (255,255,0) if i == self.selected else (200,200,200)
            label = self.font.render(text, True, color)
            x = surface.get_width() // 2 - label.get_width() // 2
            y = surface.get_height() // 2 + i * 60
            surface.blit(label, (x, y))
