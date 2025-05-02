from enum import Enum
from typing import List, Optional, Tuple, Any, Dict
import math

from npc import NPC, Attitude, DecisionModule
from item import Item
from character import Character
from src.entities.player import Player


class DroneBehavior(Enum):
    EXPLORE = "explore"
    FOLLOW = "follow"
    COLLECT = "collect"
    WAIT = "wait"

class Drone(NPC):
    """
    Дрон — сопровождение NPC с инвентарём и переключаемым поведением.

    Поведения:
        EXPLORE  — исследовать окрестности
        FOLLOW   — держаться рядом с владельцем
        COLLECT  — собирать указанный предмет
        WAIT     — оставаться на месте
    """

    def __init__(
        self,
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
        name: str,
        attitude: Attitude,
        decision_module: DecisionModule,
        route: Optional[List[Tuple[float, float]]] = None,
        behavior: DroneBehavior = DroneBehavior.WAIT,
        angle: float = 0.0,
        picture: Optional[Any] = None,
        shape: Optional[Any] = None
    ) -> None:
        super().__init__(
            entity_id=entity_id,
            x=x,
            y=y,
            health=health,
            max_health=max_health,
            speed=speed,
            attack=attack,
            defense=defense,
            vision_range=vision_range,
            hearing_range=hearing_range,
            name=name,
            attitude=attitude,
            decision_module=decision_module,
            route=route,
            angle=angle,
            picture=picture,
            shape=shape
        )
        # Инвентарь дрона
        self._inventory: List[Item] = []
        # Текущее поведение
        self._behavior: DroneBehavior = behavior

    @property
    def inventory(self) -> List[Item]:
        """Список предметов в инвентаре дрона."""
        return self._inventory

    @property
    def behavior(self) -> DroneBehavior:
        """Текущее поведение дрона."""
        return self._behavior

    def set_behavior(self, behavior: DroneBehavior) -> None:
        """Установить новое поведение дрона."""
        self._behavior = behavior

    def add_to_inventory(self, item: Item) -> None:
        """Добавляет предмет в инвентарь дрона."""
        if item.stackable:
            for inv_item in self._inventory:
                if type(inv_item) is type(item) and inv_item.name == item.name:
                    inv_item.quantity += item.quantity
                    return
        self._inventory.append(item)

    def remove_from_inventory(self, item: Item) -> None:
        """Удаляет предмет из инвентаря дрона."""
        self._inventory.remove(item)

    def transfer_item_from(self, provider: Player, item: Item) -> None:
        """Забрать предмет из инвентаря другого персонажа."""
        if item not in provider.inventory:
            raise ValueError("Предмет отсутствует у поставщика")
        provider.remove_from_inventory(item)
        self.add_to_inventory(item)

    def transfer_item_to(self, consumer: Player, item: Item) -> None:
        """Передать предмет из своего инвентаря другому персонажу."""
        if item not in self._inventory:
            raise ValueError("Предмет отсутствует в инвентаре дрона")
        self.remove_from_inventory(item)
        consumer.add_to_inventory(item)

    def collect(self, item: Item, delta_time: float) -> None:
        """
        Подлететь к указанному предмету и собрать его, когда окажется рядом.
        :param item: Объект Item для сбора
        :param delta_time: время кадра для движения
        """
        # Точка предмета
        target_x, target_y = item.position
        x, y = self.position
        dx, dy = target_x - x, target_y - y
        distance = math.hypot(dx, dy)
        # Если на расстоянии сбора (<= speed * delta_time), собираем
        move = self.speed * delta_time
        if distance <= move:
            self.position = (target_x, target_y)
            self.add_to_inventory(item)
            item.active = False
        else:
            # двигаемся к предмету
            nx, ny = dx / distance, dy / distance
            self.position = (x + nx * move, y + ny * move)

    def update(self, delta_time: float) -> None:
        """
        Обновление дрона: базовая логика NPC + логика поведения.
        """
        super().update(delta_time)
        if self._behavior == DroneBehavior.EXPLORE:
            # логика исследования
            pass
        elif self._behavior == DroneBehavior.FOLLOW:
            # логика следования за владельцем
            pass
        elif self._behavior == DroneBehavior.COLLECT:
            # находим первый доступный предмет
            perceptions: Dict[str, List[Any]] = self.perceive()
            items = [e for e in perceptions.get('visible', [])
                     if isinstance(e, Item) and e.collectable and e.active]
            if items:
                self.collect(items[0], delta_time)
        # WAIT — просто остаёмся на месте

    def render(self, surface: Any) -> None:
        """Отрисовать дрона на экране."""
        super().render(surface)
        # опционально: отображение индикатора поведения
