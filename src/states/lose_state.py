import pygame

from src.game.state_manager import StateManager
from src.settings import MENU_BG_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.states.base_state import BaseState


class LoseState(BaseState):
    """
    Состояние поражения: отображает меню с вариантами "Попробовать снова" и "Вернуться в меню".
    """
    OPTIONS = ["Попробовать снова", "Вернуться в меню"]

    def __init__(self, manager: StateManager, message: str = "Вы проиграли!") -> None:
        super().__init__(manager)
        self.__message: str = message
        self.__selected: int = 0
        self.__font: pygame.font.Font = pygame.font.SysFont(None, 58)
        bg = pygame.image.load(MENU_BG_IMAGE)
        # Подгоняем размер под экран
        self.__background: pygame.Surface = pygame.transform.scale(
            bg.convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    def change_selected(self, delta: int) -> None:
        self.__selected = (self.__selected + delta) % len(self.OPTIONS)

    def get_selected(self) -> None:
        choice: str = self.OPTIONS[self.__selected]
        if choice == "Попробовать снова":
            # Перезапустить текущий уровень
            current_id: int = self.manager.game_session.current_level.level_num
            self.manager.game_session.start_level(current_id)
            self.manager.change_state("play", game_session=self.manager.game_session)
        else:
            # Вернуться в главное меню
            self.manager.change_state("menu")

    def handle_event(self, event: pygame.event.Event) -> None:
        """Обрабатывает управление меню стрелками и выбор."""
        from src.game.input_handler import LoseStateInputHandler
        LoseStateInputHandler.handle(event, self)

    def update(self, dt: float) -> None:
        """Нет обновлений для экрана поражения."""
        pass

    def render(self, surface: pygame.Surface) -> None:
        """Отрисовать фон, сообщение и пункты меню по центру экрана."""
        surface.blit(self.__background, (0, 0))
        # Сообщение о поражении
        msg_label = self.__font.render(self.__message, True, (255, 0, 0))
        x_msg = surface.get_width() // 2 - msg_label.get_width() // 2
        y_msg = surface.get_height() // 3 - msg_label.get_height() // 2
        surface.blit(msg_label, (x_msg, y_msg))

        # Пункты меню
        for i, text in enumerate(self.OPTIONS):
            color = (255, 255, 0) if i == self.__selected else (200, 200, 200)
            label = self.__font.render(text, True, color)
            x = surface.get_width() // 2 - label.get_width() // 2
            y = surface.get_height() // 2 + i * 60
            surface.blit(label, (x, y))