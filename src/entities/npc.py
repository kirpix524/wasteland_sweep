from typing import Tuple, List, Any, Optional, Dict
from enum import Enum
import math
import random

import pygame

from src.entities.character import Character
from src.entities.entity import Entity
from src.entities.player import Player
from src.game.entity_manager import EntityManager


class Attitude(Enum):
    HOSTILE = "hostile"
    FRIENDLY = "friendly"
    NEUTRAL = "neutral"

class DecisionModule:
    """
    Модуль принятия решений для NPC.
    Реализует логику выбора действий на основе восприятия и
    возвращает целевую координату, куда должен идти NPC.
    """
    def decide(self, npc: 'NPC', perceptions: Dict[str, List[Any]]
               ) -> Optional[Tuple[float, float]]:
        ...



class ZombieDecisionModule(DecisionModule):
    """
    Модуль принятия решений для зомби.
    Реализует блуждание, погоню и атаку.
    """
    _WANDER_RADIUS: float = 120.0          # радиус случайного перемещения
    _WANDER_CHANCE: float = 0.02           # вероятность смены цели блуждания

    def __init__(self) -> None:
        self._current_target: Optional[Tuple[float, float]] = None
        self._last_player_pos: Optional[Tuple[float, float]] = None

    def decide(self, npc: 'NPC', perceptions: Dict[str, List[Any]]
               ) -> Optional[Tuple[float, float]]:
        player = self._find_player(perceptions['visible'])
        if player:  # видим игрока — запоминаем и преследуем
            self._last_player_pos = player.position
            return player.position                     # преследуем игрока

        if self._last_player_pos is not None:
            dist = math.hypot(
                self._last_player_pos[0] - npc.position[0],
                self._last_player_pos[1] - npc.position[1]
            )
            if dist > 5.0:  # ещё не дошли
                return self._last_player_pos
            self._last_player_pos = None  # пришли на место — забываем

        return self._wander(npc)                          # иначе блуждаем

    # -------- protected helpers --------
    def _find_player(self, visibles: List[Entity]) -> Optional[Any]:
        for ent in visibles:
            if isinstance(ent, Player):
                return ent
        return None

    def _wander(self, npc: 'NPC') -> Tuple[float, float]:
        if (
            self._current_target is None
            or npc.position == self._current_target
            or random.random() < self._WANDER_CHANCE
        ):
            self._current_target = self._random_point_near(npc.position)
        return self._current_target

    def _random_point_near(self, origin: Tuple[float, float]) -> Tuple[float, float]:
        angle: float = random.uniform(0.0, 2 * math.pi)
        radius: float = random.uniform(20.0, self._WANDER_RADIUS)
        return origin[0] + radius * math.cos(angle), origin[1] + radius * math.sin(angle)


class NPC(Character):
    """
    Неписи (NPC) с именем, отношением, модулем ИИ и маршрутом патрулирования.
    """
    def __init__(
        self,
        entity_manager: 'EntityManager',
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
        picture_alive: Optional[Any] = None,
        picture_dead: Optional[Any] = None,
        shape: Optional[Any] = None,
        attack_rate: float = 1.5
    ) -> None:
        super().__init__(
            entity_manager=entity_manager,
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
            picture=picture_alive,
            shape=shape
        )
        self._name: str = name
        self._attitude: Attitude = attitude
        self._decision_module: DecisionModule = decision_module
        self._route: List[Tuple[float, float]] = route or []
        self._current_waypoint_index: int = 0
        # Ссылка на текущее состояние мира для восприятия
        self._game_state: Optional[Any] = None
        self._picture_alive: Optional[Any] = picture_alive
        self._picture_dead: Optional[Any] = picture_dead
        self._attack_rate: float = attack_rate
        self._attack_timer: float = 0
        self._able_to_attack: bool = True

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
        visible: List['Entity'] = []
        audible: List['Entity'] = []
        if not self._entity_manager.all_entities:
            return {'visible': visible, 'audible': audible}
        for entity in self._entity_manager.all_entities:
            if entity is self or not entity.active:
                continue
            ex, ey = entity.position
            sx, sy = self.position
            dist = math.hypot(ex - sx, ey - sy)
            if dist <= self.vision_range:
                visible.append(entity)
            # if dist <= self.hearing_range:
            #     audible.append(entity)
        return {'visible': visible, 'audible': audible}

    def update(self, delta_time: float) -> None:
        """
        Основная логика NPC:
        1. Восприятие окружения
        2. Принятие решения модулем ИИ
        3. Действие (патрулирование или другое)
        """
        if not self.is_alive:
            return
        # Принятие решения
        perceptions = self.perceive()

        # координата, куда должен идти зомби
        target: Optional[Tuple[float, float]] = self._decision_module.decide(
            self, perceptions
        )

        if target:
            self._route.clear()
            self._route.append(target)

            # разворот к цели
            dx, dy = target[0] - self.position[0], target[1] - self.position[1]
            if dx or dy:
                self.angle = math.atan2(dy, dx)

        # движение по маршруту
        if self._route:
            self.move_towards(self._route[0], delta_time)



        # проверка возможности атаки
        player = next(
            (e for e in perceptions['visible'] if isinstance(e, Player)),
            None
        )

        if not self._able_to_attack:
            self._attack_timer += delta_time
            if self._attack_timer >= self._attack_rate:
                self._attack_timer = 0
                self._able_to_attack = True

        if player:
            if self.can_attack(player) and self._able_to_attack:
                player.take_damage(self.attack)
                self._attack_timer = 0
                self._able_to_attack = False
                return


    def move_towards(self, target: Tuple[float, float], delta_time: float) -> None:
        """
        Двигаться к указанной точке, используя _apply_movement для обработки столкновений.
        """
        tx, ty = target
        x, y = self.position
        dx, dy = tx - x, ty - y
        distance: float = math.hypot(dx, dy)

        # если уже на месте — останавливаемся
        if distance == 0:
            self._velocity.update(0, 0)
            return

        # нормализованный вектор к цели
        nx, ny = dx / distance, dy / distance

        # расстояние, которое можем пройти за этот тик
        step_distance: float = min(self.speed * delta_time, distance)

        # скорость в мировых координатах (ед./сек)
        self._velocity.update(
            nx * step_distance / delta_time,
            ny * step_distance / delta_time,
        )

        # фактическое перемещение c учётом коллизий
        self._apply_movement(delta_time)

        # сбрасываем скорость, чтобы не двигаться без приказа в следующем тике
        self._velocity.update(0, 0)

    def render(self, surface: Any) -> None:
        """
        Отрисовать NPC на экране с учётом его текущего угла поворота.
        """
        super().render(surface)  # hit-box / debug-отрисовка из Character

        picture = self._picture_alive if self.is_alive else self._picture_dead

        # поворачиваем картинку на угол (в градусах, по часовой стрелке)
        rotated = pygame.transform.rotate(picture, -math.degrees(self.angle))
        rect = rotated.get_rect(center=self.position)

        surface.blit(rotated, rect)
