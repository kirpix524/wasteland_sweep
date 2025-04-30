# src/main.py

import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.manager import GameManager

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Wasteland Sweep")
    clock = pygame.time.Clock()

    # Create the game manager (handles entities, systems, etc.)
    manager = GameManager(screen)

    # Main loop
    manager.running = True
    while manager.running:
        # Delta time in seconds
        dt = clock.tick(FPS) / 1000.0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manager.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            else:
                manager.handle_event(event)

        # Update game logic
        manager.update(dt)

        # Render frame
        manager.render()
        pygame.display.flip()

    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
