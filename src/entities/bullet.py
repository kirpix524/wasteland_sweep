import pygame
from typing import Any, Optional, Tuple, TYPE_CHECKING

from pygame.display import update

from src.entities.projectile import Projectile

if TYPE_CHECKING:
    from src.entities.entity import Shape, Entity
    from src.entities.weapon import Weapon
    from src.game.entity_manager import EntityManager


class Bullet(Projectile):
    """
    Конкретный снаряд‑пуля.

    • Летит по прямой со скоростью, унаследованной от оружия‑источника.
    • Наносит однократный урон первой столкнувшейся цели и затем деактивируется.
    • При отсутствии собственного спрайта рисуется как маленький круг.
    """

    def __init__(
        self,
        entity_manager: 'EntityManager',
        entity_id: int,
        x: float,
        y: float,
        direction: Tuple[float, float],
        source: 'Weapon',
        damage: Optional[float] = None,
        picture: Optional[Any] = None,
        shape: Optional['Shape'] = None,
        radius: int = 1,
        tracer_length: int = 70,
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        super().__init__(
            entity_manager=entity_manager,
            entity_id=entity_id,
            x=x,
            y=y,
            direction=direction,
            source=source,
            damage=damage,
            picture=picture,
            shape=shape
        )
        self._radius: int = radius
        self._tracer_length: int = tracer_length
        self._color: Tuple[int, int, int] = color

    # -----------------
    #  Properties
    # -----------------

    @property
    def radius(self) -> int:
        """Радиус круга‑заглушки (пиксели) при отсутствии спрайта."""
        return self._radius

    # -----------------
    #  Public methods
    # -----------------

    def on_collision(self, target: 'Entity') -> None:
        """
        Вызывается движком при столкновении.

        • Пытается нанести урон цели через её интерфейс take_damage().
        • После первого попадания деактивируется.
        """
        if hasattr(target, "take_damage") and callable(getattr(target, "take_damage")):
            target.take_damage(self._damage)  # type: ignore[attr-defined]
        self.active = False


    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        if not self.active:
            self._entity_manager.remove_entity_by_id(self.id)

    def render(self, surface: Any) -> None:
        """
        Рисует пулю на переданной поверхности.

        • Если передан спрайт (pygame.Surface), выводит его с центром в позиции пули.
        • Иначе рисует небольшой круг заданного цвета (ожидается API, совместимое с pygame).
        """
        if self.active:
            if self.picture is not None:  # type: ignore[attr-defined]
                rect = self.picture.get_rect(center=(int(self.position[0]), int(self.position[1])))  # type: ignore[attr-defined]
                surface.blit(self.picture, rect)
            else:
                import pygame, math

                # --- трассер -------------------------------------------------
                dx, dy = self.direction  # вектор движения
                head: tuple[int, int] = (
                    int(self.position[0]),
                    int(self.position[1]),
                )
                norm = math.hypot(dx, dy)
                if norm:
                    tail: tuple[int, int] = (
                        int(self.position[0] - dx / norm * self._tracer_length),
                        int(self.position[1] - dy / norm * self._tracer_length),
                    )
                    pygame.draw.line(surface, self._color, tail, head, width=1)

                # наконечник пули
                pygame.draw.circle(surface, self._color, head, self._radius)