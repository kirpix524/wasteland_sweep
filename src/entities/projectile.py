from abc import ABC, abstractmethod
from typing import Tuple, Optional, Any

from src.entities.entity import Entity, Shape
from src.entities.weapon import Weapon


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
        entity_id: int,
        x: float,
        y: float,
        direction: Tuple[float, float],
        source: Weapon,
        damage: float = None,
        picture: Optional[Any] = None,
        shape: Optional[Shape] = None
    ) -> None:
        super().__init__(
            entity_id=entity_id,
            x=x,
            y=y,
            angle=0.0,
            collectable=False,
            picture=picture,
            shape=shape
        )
        self._direction: Tuple[float, float] = direction
        if damage is None:
            damage = source.attack_power
        self._damage: float = damage
        self._source: Weapon = source
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
    def source(self) -> Weapon:
        """Оружие, выпустившее этот снаряд."""
        return self._source

    def update(self, delta_time: float) -> None:
        """
        Двигать снаряд и проверять достижение максимальной дальности.
        """
        dx, dy = self._direction
        move_x = dx * self._speed * delta_time
        move_y = dy * self._speed * delta_time
        x, y = self.position
        self.position = (x + move_x, y + move_y)

        # Учитываем пройденное расстояние
        self._distance_traveled += (abs(move_x) + abs(move_y))
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