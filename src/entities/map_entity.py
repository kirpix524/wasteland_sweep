from typing import Optional, Any

import pygame

from src.entities.entity import Entity, Shape, RectangleShape, CircleShape
from src.game.entity_manager import EntityManager


class MapEntity(Entity):
    def __init__(self,
                 entity_manager: 'EntityManager',
                 entity_id: int,
                 x: float,
                 y: float,
                 angle: float = 0.0,
                 picture: Optional[Any] = None,
                 shape: Optional[Shape] = None):
        super().__init__(entity_manager, entity_id, x, y, angle, False, picture, shape, is_solid=True)

    def render(self, surface: Any) -> None:
        """
        Рисует отладочный контур
        """
        debug_color: tuple[int, int, int] = (0, 255, 0)  # ярко-зелёный контур

        if isinstance(self.shape, RectangleShape):
            x, y, w, h = self.shape.get_bounding_box()
            pygame.draw.rect(surface, debug_color, pygame.Rect(x, y, w, h), width=1)
        elif isinstance(self.shape, CircleShape):
            x, y, w, h = self.shape.get_bounding_box()
            center: tuple[int, int] = (int(x), int(y))
            pygame.draw.circle(surface, debug_color, center, int(w / 2), width=1)

        sprite: Optional[pygame.Surface] = (
            # self._animation.get_image() if self._animation is not None else self._picture
            self.picture
        )

        if sprite is not None:
            # В pygame положительные углы — против часовой стрелки, поэтому берём «-angle»
            rotated_sprite: pygame.Surface = pygame.transform.rotate(sprite, -self.angle)
            rect: pygame.Rect = rotated_sprite.get_rect(center=(self.position[0], self.position[1]))
            surface.blit(rotated_sprite, rect.topleft)

    def update(self, delta_time: float) -> None:
        pass