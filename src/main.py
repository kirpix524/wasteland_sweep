# src/main.py

import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from game.state_manager import StateManager
from src.game.game_session import GameSession
from states.state_registry import register_states

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game_session = GameSession()
    state_manager = StateManager(game_session)
    register_states(state_manager)
    state_manager.change_state("menu")

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
                state_manager.current_state.handle_event(event)

        # Update game logic
        if state_manager.current_state:
            state_manager.current_state.update(dt)
            if state_manager.quit:
                running = False
            state_manager.current_state.render(screen)

        pygame.display.flip()


    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
