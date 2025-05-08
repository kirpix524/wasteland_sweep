from abc import abstractmethod
from enum import Enum, auto
from typing import Any, Optional, List, TYPE_CHECKING, Tuple

import pygame
import pygame.mixer

from src.entities.entity import Entity
from src.entities.item import Item
from src.game.entity_manager import EntityManager

if TYPE_CHECKING:
    from src.entities.entity import Shape
    from src.entities.modifier import Modifier
    from src.entities.projectile import Projectile

class FireMode(Enum):
    SINGLE: int = auto()   # одиночный
    AUTO: int = auto()     # автоматический
    BURST: int = auto()    # очередь

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
        available_fire_modes: Optional[List[FireMode]] = None,
        firing_rate: Optional[int] = None,
        shape: Optional['Shape'] = None,
        fire_sound: Optional[str] = None
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
        self._firing_rate: int           = firing_rate
        self._bullet_speed: float        = bullet_speed
        self._attack_power: float        = attack_power
        self._reload_time: float         = reload_time
        self._shot_hearing_range: float  = shot_hearing_range
        self._shot_vision_range: float   = shot_vision_range
        self._fire_sound: Optional[pygame.mixer.Sound] = (
            pygame.mixer.Sound(fire_sound) if fire_sound else None
        )

        # Доступные режимы стрельбы
        if available_fire_modes is None:
            self._available_fire_modes: List[FireMode] = [FireMode.SINGLE]
        else:
            self._available_fire_modes: List[FireMode] = available_fire_modes

        self._current_fire_mode: FireMode = self._available_fire_modes[0]

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
        self._owner: Optional['Entity'] = None

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

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = value

    @property
    def current_fire_mode(self) -> FireMode:
        """Текущий выбранный режим стрельбы."""
        return self._current_fire_mode

    @property
    def available_fire_modes(self) -> Tuple[FireMode, ...]:
        """Все режимы стрельбы, поддерживаемые конкретным образцом оружия."""
        return tuple(self._available_fire_modes)

    @property
    def firing_rate(self) -> int:
        return self._firing_rate

    def _play_fire_sound(self) -> None:
        if self._fire_sound is None:
            return

        # ищем свободный канал; если None ─ освобождаем старейший
        channel: pygame.mixer.Channel | None = pygame.mixer.find_channel()
        if channel is None:
            channel = pygame.mixer.find_channel(force=True)  # прервать самый старый

        channel.play(self._fire_sound)

    def set_fire_mode(self, mode: FireMode) -> None:
        """
        Установить режим стрельбы, если он доступен у данного оружия.

        :raises ValueError: если режим не поддерживается.
        """
        if mode in self._available_fire_modes:
            self._current_fire_mode = mode

    def cycle_fire_mode(self) -> None:
        """Переключить режим стрельбы по кругу (Single → Auto → Burst → ...)."""
        index: int = self._available_fire_modes.index(self._current_fire_mode)
        next_index: int = (index + 1) % len(self._available_fire_modes)
        self._current_fire_mode = self._available_fire_modes[next_index]


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
                self.reload_magazine()

    def start_reload(self, available_ammo: Optional[int]) -> None:
        """Начать перезарядку, если оружие не в процессе перезарядки."""
        if not self._is_reloading:
            self._is_reloading = True
            self._reload_timer = 0.0
            if available_ammo is not None:
                self._available_ammo = available_ammo
            else:
                self._available_ammo = self._magazine_capacity

    def stop_reload(self) -> None:
        self._is_reloading = False

    def can_fire(self) -> bool:
        """Проверяет, можно ли сделать выстрел (не в перезарядке)."""
        return not self._is_reloading

    def fire(self, player_position: Tuple[float, float], direction: pygame.Vector2) -> Optional['Projectile']:
        """
        Выполнить выстрел в заданном направлении.

        :param player_position: Текущие координаты игрока.
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
        bullet = Bullet(
            entity_manager=self._entity_manager,
            entity_id=0,
            x=player_position[0],
            y=player_position[1],
            direction=(direction.x, direction.y),
            source=self,
        )

        self._entity_manager.add_existing_entity(bullet)

        # 4. Обновляем счётчик патронов
        self._current_ammo -= 1
        if self._current_ammo == 0:
            self.start_reload(None)

        self._play_fire_sound()
        return bullet
