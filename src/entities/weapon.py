from abc import abstractmethod
from typing import Any, Optional, List, TYPE_CHECKING

import pygame

from src.entities.item import Item
from src.game.entity_manager import EntityManager

if TYPE_CHECKING:
    from src.entities.entity import Shape
    from src.entities.modifier import Modifier
    from src.entities.projectile import Projectile


class Weapon(Item):
    """
    Класс оружия — предмет, который можно подобрать и использовать для стрельбы.

    Поддерживает базовые характеристики и списки модификаторов:
        firing_range, bullet_speed, attack_power, reload_time,
        shot_hearing_range, shot_vision_range
    """

    def __init__(
        self,
        entity_manager: EntityManager,
        entity_id: int,
        x: float,
        y: float,
        name: str,
        description: str,
        firing_range: float,
        bullet_speed: float,
        attack_power: float,
        reload_time: float,
        shot_hearing_range: float,
        shot_vision_range: float,
        magazine_capacity: int,
        picture: Optional[Any] = None,
        shape: Optional['Shape'] = None
    ) -> None:
        super().__init__(
            entity_manager=entity_manager,
            entity_id=entity_id,
            x=x,
            y=y,
            name=name,
            description=description,
            picture=picture,
            shape=shape,
            stackable=False,
            quantity=1
        )
        # Базовые значения
        self._firing_range: float        = firing_range
        self._bullet_speed: float        = bullet_speed
        self._attack_power: float        = attack_power
        self._reload_time: float         = reload_time
        self._shot_hearing_range: float  = shot_hearing_range
        self._shot_vision_range: float   = shot_vision_range

        # Вместимость магазина и оставшиеся выстрелы
        self._magazine_capacity: int = magazine_capacity
        self._current_ammo: int = magazine_capacity
        self._available_ammo: int = 0

        # Списки модификаторов
        self._firing_range_mods:       List['Modifier'] = []
        self._bullet_speed_mods:       List['Modifier'] = []
        self._attack_power_mods:       List['Modifier'] = []
        self._reload_time_mods:        List['Modifier'] = []
        self._shot_hearing_range_mods: List['Modifier'] = []
        self._shot_vision_range_mods:  List['Modifier'] = []

        # Внутренние флаги
        self._is_reloading: bool = False
        self._reload_timer: float = 0.0

    @property
    def current_ammo(self) -> int:
        return self._current_ammo

    @property
    def firing_range(self) -> float:
        return self._firing_range + sum(m.value for m in self._firing_range_mods)

    def add_firing_range_modifier(self, mod: 'Modifier') -> None:
        self._firing_range_mods.append(mod)

    def remove_firing_range_modifier(self, mod: 'Modifier') -> None:
        self._firing_range_mods.remove(mod)

    @property
    def bullet_speed(self) -> float:
        return self._bullet_speed + sum(m.value for m in self._bullet_speed_mods)

    def add_bullet_speed_modifier(self, mod: 'Modifier') -> None:
        self._bullet_speed_mods.append(mod)

    def remove_bullet_speed_modifier(self, mod: 'Modifier') -> None:
        self._bullet_speed_mods.remove(mod)

    @property
    def attack_power(self) -> float:
        return self._attack_power + sum(m.value for m in self._attack_power_mods)

    def add_attack_power_modifier(self, mod: 'Modifier') -> None:
        self._attack_power_mods.append(mod)

    def remove_attack_power_modifier(self, mod: 'Modifier') -> None:
        self._attack_power_mods.remove(mod)

    @property
    def reload_time(self) -> float:
        return self._reload_time + sum(m.value for m in self._reload_time_mods)

    def add_reload_time_modifier(self, mod: 'Modifier') -> None:
        self._reload_time_mods.append(mod)

    def remove_reload_time_modifier(self, mod: 'Modifier') -> None:
        self._reload_time_mods.remove(mod)

    @property
    def shot_hearing_range(self) -> float:
        return self._shot_hearing_range + sum(m.value for m in self._shot_hearing_range_mods)

    def add_shot_hearing_range_modifier(self, mod: 'Modifier') -> None:
        self._shot_hearing_range_mods.append(mod)

    def remove_shot_hearing_range_modifier(self, mod: 'Modifier') -> None:
        self._shot_hearing_range_mods.remove(mod)

    @property
    def shot_vision_range(self) -> float:
        return self._shot_vision_range + sum(m.value for m in self._shot_vision_range_mods)

    def add_shot_vision_range_modifier(self, mod: 'Modifier') -> None:
        self._shot_vision_range_mods.append(mod)

    def remove_shot_vision_range_modifier(self, mod: 'Modifier') -> None:
        self._shot_vision_range_mods.remove(mod)


    def reload_magazine(self) -> None:
        """Перезарядить магазин до полной вместимости."""
        self._current_ammo = max(self._magazine_capacity, self._available_ammo)
        self._available_ammo = 0

    def update(self, delta_time: float) -> None:
        """Обрабатывает таймер перезарядки."""
        if self._is_reloading:
            self._reload_timer += delta_time
            if self._reload_timer >= self.reload_time:
                self._is_reloading = False
                self._reload_timer = 0.0

    def start_reload(self, available_ammo: Optional[int]) -> None:
        """Начать перезарядку, если оружие не в процессе перезарядки."""
        if not self._is_reloading:
            self._is_reloading = True
            self._reload_timer = 0.0
            if available_ammo is not None:
                self._available_ammo = available_ammo
            else:
                self._available_ammo = self._magazine_capacity

    def can_fire(self) -> bool:
        """Проверяет, можно ли сделать выстрел (не в перезарядке)."""
        return not self._is_reloading

    def fire(self, direction: pygame.Vector2) -> Optional['Projectile']:
        """
        Выполнить выстрел в заданном направлении.

        :param direction: Нормализованный вектор направления полёта.
        :return: Bullet либо None, если выстрел невозможен.
        """
        from src.entities.bullet import Bullet
        # 1. Проверяем, что можем стрелять
        if not self.can_fire():
            return None
        if self._current_ammo <= 0:
            self.start_reload(None)  # Автоматически запускаем перезарядку
            return None

        # 2. Нормализуем направление
        if direction.length_squared() == 0:
            return None
        direction = direction.normalize()

        # 3. Создаём пулю
        bullet: Projectile = Bullet(
            entity_manager=self._manager,
            entity_id=0,
            x=self.position[0],
            y=self.position[1],
            direction=(direction.x, direction.y),
            source=self,
        )

        self._manager.add_existing_entity(bullet)

        # 4. Обновляем счётчик патронов
        self._current_ammo -= 1
        if self._current_ammo == 0:
            self.start_reload(None)

        return bullet
