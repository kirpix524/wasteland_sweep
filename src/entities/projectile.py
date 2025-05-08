import math
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Any, TYPE_CHECKING

from src.entities.entity import Entity, Shape


if TYPE_CHECKING:
    from src.entities.weapon import Weapon
    from src.game.entity_manager import EntityManager


class Projectile(Entity, ABC):
    """
    Базовый класс для снарядов.

    :param entity_id: Уникальный идентификатор
    :param x, y: стартовая позиция
    :param direction: нормализованный вектор направления полёта (dx, dy)
    :param damage: урон при попадании
    :param source: оружие, выпустившее снаряд (Weapon)
    :param picture: опциональная картинка (pygame.Surface и т.п.)
    :param shape: форма снаряда для столкновений
    """
    def __init__(
        self,
        entity_manager: 'EntityManager',
        entity_id: int,
        x: float,
        y: float,
        direction: Tuple[float, float],
        source: 'Weapon',
        damage: float = None,
        picture: Optional[Any] = None,
        shape: Optional[Shape] = None
    ) -> None:
        super().__init__(
            entity_manager=entity_manager,
            entity_id=entity_id,
            x=x,
            y=y,
            angle=0.0,
            collectable=False,
            picture=picture,
            shape=shape,
            is_solid=False
        )
        self._direction: Tuple[float, float] = direction
        if damage is None:
            damage = source.attack_power
        self._damage: float = damage
        self._source: 'Weapon' = source
        # Speed and range are taken from the weapon that fired the projectile
        self._speed: float = source.bullet_speed
        self._max_range: float = source.firing_range
        self._distance_traveled: float = 0.0

    @property
    def direction(self) -> Tuple[float, float]:
        return self._direction

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def damage(self) -> float:
        return self._damage

    @property
    def max_range(self) -> float:
        return self._max_range

    @property
    def source(self) -> 'Weapon':
        """Оружие, выпустившее этот снаряд."""
        return self._source

    def update(self, delta_time: float) -> None:
        """
        Перемещает снаряд, проверяя столкновения на каждом небольшом под-шаге,
        чтобы исключить «проскок» объектов при высокой скорости.
        """
        if not self.active:
            return

        dx, dy = self._direction
        length: float = math.hypot(dx, dy)
        if length == 0:
            return

        ndx: float = dx / length
        ndy: float = dy / length

        total_dist: float = self._speed * delta_time
        step_dist: float = 4.0  # максимальный под-шаг (px)

        travelled: float = 0.0
        source_owner: Entity | None = getattr(self._source, "owner", None)

        while travelled < total_dist and self.active:
            dist: float = min(step_dist, total_dist - travelled)
            move_x: float = ndx * dist
            move_y: float = ndy * dist

            x, y = self.position
            self.position = (x + move_x, y + move_y)

            # — проверка столкновений каждые step_dist пикселей —
            for entity in self._entity_manager.all_entities:
                if (
                        entity is self
                        or entity is source_owner
                        or not entity.active
                        or not entity.is_solid
                ):
                    continue
                if self.collides_with(entity):
                    self.on_collision(entity)
                    self.active = False
                    break

            travelled += dist
            self._distance_traveled += dist

        # — проверка достижения максимальной дальности —
        if self._distance_traveled >= self._max_range:
            self.active = False

    @abstractmethod
    def on_collision(self, target: Entity) -> None:
        """
        Вызывается при столкновении с другой сущностью.
        Здесь обычно наносится урон или проявляется эффект.
        """
        ...

    @abstractmethod
    def render(self, surface: Any) -> None:
        """
        Отрисовать снаряд на переданной поверхности.
        """
        ...