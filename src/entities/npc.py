from typing import Tuple, List, Any, Optional, Dict
from enum import Enum
import math

from character import Character

class Attitude(Enum):
    HOSTILE = "hostile"
    FRIENDLY = "friendly"
    NEUTRAL = "neutral"

class DecisionModule:
    """
    Модуль принятия решений для NPC.
    Реализует логику выбора действий на основе восприятия.
    """
    def decide(self, npc: 'NPC', perceptions: Dict[str, List[Any]]) -> None:
        """
        Выполняет шаг принятия решения, используя данные о восприятии:
        :param npc: экземпляр NPC
        :param perceptions: словарь с ключами 'visible' и 'audible'
        """
        ...  # Переопределяется конкретными модулями

class NPC(Character):
    """
    Неписи (NPC) с именем, отношением, модулем ИИ и маршрутом патрулирования.
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
            angle=angle,
            collectable=False,
            picture=picture,
            shape=shape
        )
        self._name: str = name
        self._attitude: Attitude = attitude
        self._decision_module: DecisionModule = decision_module
        self._route: List[Tuple[float, float]] = route or []
        self._current_waypoint_index: int = 0
        # Ссылка на текущее состояние мира для восприятия
        self._game_state: Optional[Any] = None

    @property
    def name(self) -> str:
        """Имя NPC."""
        return self._name

    @property
    def attitude(self) -> Attitude:
        """Отношение NPC к игроку/миру."""
        return self._attitude

    @property
    def decision_module(self) -> DecisionModule:
        """Модуль принятия решений."""
        return self._decision_module

    @property
    def route(self) -> List[Tuple[float, float]]:
        """Маршрут патрулирования NPC (список координат)."""
        return self._route

    def set_game_state(self, game_state: Any) -> None:
        """
        Устанавливает текущее состояние мира для восприятия.
        """
        self._game_state = game_state

    def perceive(self) -> Dict[str, List[Any]]:
        """
        Составляет список видимых и слышимых объектов вокруг NPC,
        используя сохранённое состояние мира (self._game_state).
        """
        visible: List[Any] = []
        audible: List[Any] = []
        if not self._game_state:
            return {'visible': visible, 'audible': audible}
        for entity in self._game_state.entities:
            if entity is self or not entity.active:
                continue
            ex, ey = entity.position
            sx, sy = self.position
            dist = math.hypot(ex - sx, ey - sy)
            if dist <= self.vision_range:
                visible.append(entity)
            if dist <= self.hearing_range:
                audible.append(entity)
        return {'visible': visible, 'audible': audible}

    def update(self, delta_time: float) -> None:
        """
        Основная логика NPC:
        1. Восприятие окружения
        2. Принятие решения модулем ИИ
        3. Действие (патрулирование или другое)
        """
        # Восприятие мира
        perceptions = self.perceive()
        # Принятие решения
        self._decision_module.decide(self, perceptions)
        # Патрулирование по маршруту
        if self._route:
            target = self._route[self._current_waypoint_index]
            self.move_towards(target, delta_time)
            if self.position == target:
                self._current_waypoint_index = (
                    self._current_waypoint_index + 1
                ) % len(self._route)

    def move_towards(self, target: Tuple[float, float], delta_time: float) -> None:
        """
        Двигаться к указанной точке с учётом speed и delta_time.
        """
        tx, ty = target
        x, y = self.position
        dx, dy = tx - x, ty - y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        nx, ny = dx / distance, dy / distance
        move = self.speed * delta_time
        if move >= distance:
            self.position = target
        else:
            self.position = (x + nx * move, y + ny * move)

    def render(self, surface: Any) -> None:
        """
        Отрисовать NPC на экране.
        """
        super().render(surface)

        # (опционально) отладочная отрисовка маршрута
        # for pt in self._route:
        #     pygame.draw.circle(surface, (255,0,0), (int(pt[0]), int(pt[1])), 3)
