# src/main.py

import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from game.state_manager import StateManager
from src.game.input_handler import InputHandler
from src.game.renderer import Renderer
from states.state_registry import register_states

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()


    manager = StateManager()
    register_states(manager)
    manager.change_state("menu")

    # Main loop
    running = True
    while running:
        # Delta time in seconds
        dt = clock.tick(FPS) / 1000.0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            else:
                InputHandler.handle(event, manager.current_state)

        # Update game logic
        if manager.current_state:
            manager.current_state.update(dt)
            if manager.quit:
                running = False

            manager.current_state.update(dt)
            Renderer.render(screen, manager.current_state)

        pygame.display.flip()


    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
