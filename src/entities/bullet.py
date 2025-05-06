import pygame
from typing import Any, Optional, Tuple

from src.entities.entity import Shape, Entity
from src.entities.projectile import Projectile
from src.entities.weapon import Weapon


class Bullet(Projectile):
    """
    Конкретный снаряд‑пуля.

    • Летит по прямой со скоростью, унаследованной от оружия‑источника.
    • Наносит однократный урон первой столкнувшейся цели и затем деактивируется.
    • При отсутствии собственного спрайта рисуется как маленький круг.
    """

    def __init__(
        self,
        entity_id: int,
        x: float,
        y: float,
        direction: Tuple[float, float],
        source: Weapon,
        damage: Optional[float] = None,
        picture: Optional[Any] = None,
        shape: Optional[Shape] = None,
        radius: int = 1,
        color: Tuple[int, int, int] = (255, 255, 0),
    ) -> None:
        super().__init__(
            entity_id=entity_id,
            x=x,
            y=y,
            direction=direction,
            source=source,
            damage=damage,
            picture=picture,
            shape=shape,
        )
        self._radius: int = radius
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

    def on_collision(self, target: Entity) -> None:
        """
        Вызывается движком при столкновении.

        • Пытается нанести урон цели через её интерфейс take_damage().
        • После первого попадания деактивируется.
        """
        if hasattr(target, "take_damage") and callable(getattr(target, "take_damage")):
            target.take_damage(self._damage, self._source)  # type: ignore[attr-defined]
        self.active = False

    def render(self, surface: Any) -> None:
        """
        Рисует пулю на переданной поверхности.

        • Если передан спрайт (pygame.Surface), выводит его с центром в позиции пули.
        • Иначе рисует небольшой круг заданного цвета (ожидается API, совместимое с pygame).
        """
        if self.picture is not None:  # type: ignore[attr-defined]
            rect = self.picture.get_rect(center=(int(self.position[0]), int(self.position[1])))  # type: ignore[attr-defined]
            surface.blit(self.picture, rect)
        else:
            # Ленивая локальная импорт‑заглушка — избавляет остальных от жёсткой зависимости
            import pygame  # noqa: WPS433  (локальный импорт допустим для снижения связности)
            pygame.draw.circle(
                surface,
                self._color,
                (int(self.position[0]), int(self.position[1])),
                self._radius,
            )