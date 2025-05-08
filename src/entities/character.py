import pygame

from abc import ABC, abstractmethod
from typing import Any, Optional, List

from src.entities.entity import Entity, Shape
from src.entities.modifier import Modifier
from src.game.animation import Animation
from src.game.entity_manager import EntityManager


class Character(Entity, ABC):
    """
    Базовый класс для живых персонажей.
    Хранит базовые характеристики и списки модификаторов для каждой из них.
    """

    def __init__(
        self,
        entity_manager: EntityManager,
        entity_id: int,
        x: float,
        y: float,
        health: float,
        max_health: float,
        speed: float,
        attack: float,
        defense: float,
        vision_range: float,
        hearing_range: float,
        angle: float = 0.0,
        collectable: bool = False,
        can_collect: bool = False,
        picture: Optional[Any] = None,
        animation: Optional[Animation] = None,
        shape: Optional[Shape] = None
    ) -> None:
        super().__init__(entity_manager, entity_id, x, y, angle, collectable, picture, shape, is_solid=True)

        # базовые значения
        self._health: float = health
        self._max_health: float = max_health
        self._speed: float = speed
        self._attack: float = attack
        self._defense: float = defense
        self._velocity: pygame.Vector2 = pygame.Vector2(0.0, 0.0)
        self._vision_range: float = vision_range
        self._hearing_range: float = hearing_range
        self._can_collect: bool = can_collect

        # списки модификаторов
        self._max_health_modifiers: List[Modifier] = []
        self._speed_modifiers:      List[Modifier] = []
        self._attack_modifiers:     List[Modifier] = []
        self._defense_modifiers:    List[Modifier] = []
        self._vision_modifiers:     List[Modifier] = []
        self._hearing_modifiers:    List[Modifier] = []
        self._animation: Animation = animation

    @property
    def health(self) -> float:
        return self._health

    @property
    def max_health(self) -> float:
        return self._max_health + sum(m.value for m in self._max_health_modifiers)

    @property
    def speed(self) -> float:
        return self._speed + sum(m.value for m in self._speed_modifiers)

    @property
    def attack(self) -> float:
        return self._attack + sum(m.value for m in self._attack_modifiers)

    @property
    def defense(self) -> float:
        return self._defense + sum(m.value for m in self._defense_modifiers)

    @property
    def vision_range(self) -> float:
        return self._vision_range + sum(m.value for m in self._vision_modifiers)

    @property
    def hearing_range(self) -> float:
        return self._hearing_range + sum(m.value for m in self._hearing_modifiers)

    @property
    def can_collect(self) -> bool:
        return self._can_collect

    @property
    def animation(self) -> Animation:
        return self._animation

    @animation.setter
    def animation(self, animation: Animation) -> None:
        self._animation = animation

    def take_damage(self, amount: float) -> None:
        """Уменьшает здоровье с учётом текущей защиты."""
        damage = max(0.0, amount - self.defense)
        self._health = max(0.0, self._health - damage)

    def heal(self, amount: float) -> None:
        """Восстанавливает здоровье, но не больше текущего максимума."""
        self._health = min(self.max_health, self._health + amount)

    # методы для управления модификаторами
    def add_max_health_modifier(self, mod: Modifier) -> None:
        self._max_health_modifiers.append(mod)
        self._health = min(self.max_health, self._health)

    def remove_max_health_modifier(self, mod: Modifier) -> None:
        self._max_health_modifiers.remove(mod)
        self._health = min(self.max_health, self._health)

    def add_speed_modifier(self, mod: Modifier) -> None:
        self._speed_modifiers.append(mod)
    def remove_speed_modifier(self, mod: Modifier) -> None:
        self._speed_modifiers.remove(mod)

    def add_attack_modifier(self, mod: Modifier) -> None:
        self._attack_modifiers.append(mod)
    def remove_attack_modifier(self, mod: Modifier) -> None:
        self._attack_modifiers.remove(mod)

    def add_defense_modifier(self, mod: Modifier) -> None:
        self._defense_modifiers.append(mod)
    def remove_defense_modifier(self, mod: Modifier) -> None:
        self._defense_modifiers.remove(mod)

    def add_vision_modifier(self, mod: Modifier) -> None:
        self._vision_modifiers.append(mod)
    def remove_vision_modifier(self, mod: Modifier) -> None:
        self._vision_modifiers.remove(mod)

    def add_hearing_modifier(self, mod: Modifier) -> None:
        self._hearing_modifiers.append(mod)
    def remove_hearing_modifier(self, mod: Modifier) -> None:
        self._hearing_modifiers.remove(mod)

    def update(self, delta_time: float) -> None:
        """
        Обновляет позицию персонажа на основе вектора скорости.
        """
        self._apply_movement(delta_time)

    def render(self, surface: Any) -> None:
        pass

    def _apply_movement(self, delta_time: float) -> None:
        """
        Перемещает персонажа, учитывая столкновения.
        """
        if self._velocity.length_squared() == 0:
            return

        dx: float = self._velocity.x * delta_time
        dy: float = self._velocity.y * delta_time

        x, y = self.position
        # полный шаг
        if self._entity_manager.can_move(self, (x + dx, y + dy)):
            self.position = (x + dx, y + dy)
            return

        # попытка по оси X
        if dx and self._entity_manager.can_move(self, (x + dx, y)):
            self.position = (x + dx, y)
            x += dx

        # попытка по оси Y
        if dy and self._entity_manager.can_move(self, (x, y + dy)):
            self.position = (x, y + dy)
