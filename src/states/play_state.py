import pygame
from typing import Tuple
from src.states.base_state import BaseState

class Character:
    def __init__(self, image_path: str, start_pos: Tuple[int, int]) -> None:
        # Protected attributes
        self._original_image: pygame.Surface = pygame.image.load(image_path).convert_alpha()
        self._image: pygame.Surface = self._original_image
        self._position: pygame.Vector2 = pygame.Vector2(start_pos)
        self._rect: pygame.Rect = self._image.get_rect(center=start_pos)
        self._speed: float = 100.0  # пикселей в секунду

    def update(self, dt: float) -> None:
        # Перемещение по WASD
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_s]:
            direction.y = 1
        if keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_d]:
            direction.x = 1
        if direction.length_squared() > 0:
            direction = direction.normalize()
            self._position += direction * self._speed * dt
            self._rect.center = (round(self._position.x), round(self._position.y))

        # Поворот к курсору мыши
        mouse_pos = pygame.mouse.get_pos()
        vector_to_mouse = pygame.Vector2(mouse_pos) - self._position
        if vector_to_mouse.length_squared() > 0:
            # Угол в градусах между вектором вправо и вектором до мыши
            angle = vector_to_mouse.angle_to(pygame.Vector2(1, 0))
            # Обратное направление для pygame.rotate
            self._image = pygame.transform.rotate(self._original_image, -angle)
            # Обновляем rect, сохраняя центр
            self._rect = self._image.get_rect(center=self._rect.center)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self._image, self._rect)


class PlayState(BaseState):
    def __init__(self, manager, background_path: str, character_path: str) -> None:
        super().__init__(manager)
        # Protected attributes
        self._background: pygame.Surface = pygame.image.load(background_path).convert()
        # Растягиваем под размер экрана
        screen_rect = manager.screen.get_rect()
        self._background = pygame.transform.scale(
            self._background,
            (screen_rect.width, screen_rect.height)
        )
        # Создаём персонажа в центре
        center = screen_rect.center
        self._character: Character = Character(character_path, center)

    def handle_event(self, event: pygame.event.Event) -> None:
        # Escape возвращает в меню
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.change_state("menu")

    def update(self, dt: float) -> None:
        self._character.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self._background, (0, 0))
        self._character.render(surface)
