import math

import pygame

from abc import ABC, abstractmethod
from typing import Any, Optional, List

from src.entities.entity import Entity, Shape, RectangleShape, CircleShape
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
        angle: float = 0.0,
        collectable: bool = False,
        can_collect: bool = False,
        picture: Optional[Any] = None,
        animation: Optional[Animation] = None,
        shape: Optional[Shape] = None,
        vision_angle: float = 120.0,
        attack_range: float = 5.0
    ) -> None:
        super().__init__(entity_manager, entity_id, x, y, angle, collectable, picture, shape, is_solid=True)

        # базовые значения
        self._health: float = health
        self._max_health: float = max_health
        self._speed: float = speed
        self._attack: float = attack
        self._attack_range: float = attack_range
        self._defense: float = defense
        self._velocity: pygame.Vector2 = pygame.Vector2(0.0, 0.0)
        self._vision_range: float = vision_range
        self._can_collect: bool = can_collect
        self._is_alive: bool = True
        self._vision_angle: float = vision_angle

        # списки модификаторов
        self._max_health_modifiers: List[Modifier] = []
        self._speed_modifiers:      List[Modifier] = []
        self._attack_modifiers:     List[Modifier] = []
        self._defense_modifiers:    List[Modifier] = []
        self._vision_modifiers:     List[Modifier] = []
        self._hearing_modifiers:    List[Modifier] = []
        self._animation: Animation = animation

    @property
    def is_solid(self) -> bool:
        if self._is_alive:
            return self._is_solid
        else:
            return False

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
    def can_collect(self) -> bool:
        return self._can_collect

    @property
    def animation(self) -> Animation:
        return self._animation

    @animation.setter
    def animation(self, animation: Animation) -> None:
        self._animation = animation

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @property
    def vision_angle(self) -> float:
        return self._vision_angle

    def can_attack(self, target: 'Character') -> bool:
        """
        Проверяет, находится ли ``target`` в зоне досягаемости атаки.

        Создаёт увеличенную копию собственной формы на величину ``_attack_range``
        и проверяет пересечение с формой цели.

        :param target: персонаж-цель
        :return: ``True``, если цель доступна для атаки
        """
        if target is self or not target.is_alive:
            return False

        # --- создаём увеличенную копию формы ---
        enlarged_shape: Shape
        if isinstance(self.shape, RectangleShape):
            x, y, w, h = self.shape.get_bounding_box()
            enlarged_shape = RectangleShape(
                x=x,
                y=y,
                width=w + 2 * self._attack_range,
                height=h + 2 * self._attack_range,
            )
        elif isinstance(self.shape, CircleShape):
            x, y, r, _ = self.shape.get_bounding_box()
            enlarged_shape = CircleShape(
                center_x=x,
                center_y=y,
                radius=r + self._attack_range,
            )
        else:
            # Fallback: проверяем по дистанции между центрами
            sx, sy = self.position
            tx, ty = target.position
            return math.hypot(tx - sx, ty - sy) <= self._attack_range

        # --- проверяем пересечение увеличенной формы с формой цели ---
        return enlarged_shape.intersects(target.shape)

    def take_damage(self, amount: float) -> None:
        """Уменьшает здоровье с учётом текущей защиты."""
        damage = max(0.0, amount - self.defense)
        self._health = max(0.0, self._health - damage)
        if self._health == 0.0:
            self._is_alive = False

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

    def render(self, surface: pygame.Surface) -> None:
        """
        Рисует отладочный контур формы персонажа.
        """
        # debug_color_green: tuple[int, int, int] = (0, 255, 0)  # ярко-зелёный контур
        # debug_color_red: tuple[int, int, int] = (255, 0, 0)  # ярко-красный контур
        #
        # if isinstance(self.shape, RectangleShape):
        #     x, y, w, h = self.shape.get_bounding_box()
        #     center: tuple[int, int] = (int(x), int(y))
        #     pygame.draw.rect(surface, debug_color_green, pygame.Rect(x, y, w, h), width=1)
        #     pygame.draw.circle(surface, debug_color_red, center, 3)  # точка-центр
        # elif isinstance(self.shape, CircleShape):
        #     x, y, w, h = self.shape.get_bounding_box()
        #     pygame.draw.circle(surface, debug_color_green, self.position, int(w / 2), width=1)
        #     pygame.draw.circle(surface, debug_color_red, self.position, 3)  # точка-центр


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
