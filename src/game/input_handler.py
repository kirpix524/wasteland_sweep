import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.player import PlayerController
    from src.states.main_menu_state import MainMenuState


class MainMenuStateInputHandler:
    @staticmethod
    def handle(event: pygame.event.Event, state: 'MainMenuState') -> None:
        # Преобразуем кнопку в команду, либо сразу передаём
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                state.change_selected(1)
            elif event.key == pygame.K_UP:
                state.change_selected(-1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                state.get_selected()

class PlayStateInputHandler:
    @staticmethod
    def handle(event: pygame.event.Event, controller: 'PlayerController') -> None:
        """
        Преобразует события Pygame в команды для PlayerController.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                controller.start_move_left()
            elif event.key == pygame.K_d:
                controller.start_move_right()
            elif event.key == pygame.K_w:
                controller.start_move_up()
            elif event.key == pygame.K_s:
                controller.start_move_down()
            elif event.key == pygame.K_r:
                controller.reload()
            elif event.key == pygame.K_y:  # переключаем режим огня
                controller.cycle_fire_mode()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                controller.stop_move_horizontal()
            elif event.key in (pygame.K_w, pygame.K_s):
                controller.stop_move_vertical()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая кнопка
                controller.mouse_button_down(pygame.Vector2(event.pos))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # левая кнопка
                controller.mouse_button_up()
        elif event.type == pygame.MOUSEWHEEL:  # поддержка pygame-2
            if event.y > 0:
                controller.cycle_weapon(1)
            elif event.y < 0:
                controller.cycle_weapon(-1)
        elif event.type == pygame.MOUSEMOTION:
            controller.update_aim(pygame.Vector2(event.pos))
