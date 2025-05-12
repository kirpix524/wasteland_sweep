from typing import Tuple, List, Any, Optional, Dict
from enum import Enum
import math
import random

import pygame

from src.entities.character import Character
from src.entities.entity import Entity, CircleShape, RectangleShape, Shape
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
        self._decision_timer: float = 0

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

    def _segment_intersects_shape(
            self,
            start: Tuple[float, float],
            end: Tuple[float, float],
            shape: Shape,
    ) -> bool:
        """
        Возвращает ``True``, если отрезок (start-end) пересекает ``shape``.
        Поддерживаются ``RectangleShape`` и ``CircleShape``.
        """
        sx, sy = start
        ex, ey = end

        if isinstance(shape, RectangleShape):
            min_x, min_y, w, h = shape.get_bounding_box()
            max_x: float = min_x + w
            max_y: float = min_y + h

            dx: float = ex - sx
            dy: float = ey - sy
            t_enter: float = 0.0
            t_exit: float = 1.0

            for p, q1, q2 in (
                    (-dx, sx - min_x, sx - max_x),
                    (dx, max_x - sx, min_x - sx),
                    (-dy, sy - min_y, sy - max_y),
                    (dy, max_y - sy, min_y - sy),
            ):
                if p == 0.0:
                    if q1 < 0.0:
                        return False  # параллельно и вне прямоугольника
                    continue
                t0: float = q1 / p
                t1: float = q2 / p
                t_enter = max(t_enter, min(t0, t1))
                t_exit = min(t_exit, max(t0, t1))
                if t_enter > t_exit:
                    return False
            return True

        if isinstance(shape, CircleShape):
            dx: float = ex - sx
            dy: float = ey - sy
            fx: float = sx - shape.center_x
            fy: float = sy - shape.center_y

            a: float = dx * dx + dy * dy
            b: float = 2 * (fx * dx + fy * dy)
            c: float = fx * fx + fy * fy - (shape.radius * shape.radius)
            discriminant: float = b * b - 4 * a * c
            if discriminant < 0.0:
                return False
            if a ==0.0:
                return False
            discriminant = math.sqrt(discriminant)
            t1: float = (-b - discriminant) / (2 * a)
            t2: float = (-b + discriminant) / (2 * a)
            return (0.0 <= t1 <= 1.0) or (0.0 <= t2 <= 1.0)

        return False

    def perceive(self) -> Dict[str, List['Entity']]:
        """
        Составляет список видимых и слышимых объектов вокруг NPC,
        учитывая препятствия (is_solid) между NPC и целью.
        """
        visible: List['Entity'] = []

        entities: List['Entity'] = self._entity_manager.all_entities
        if not entities:
            return {'visible': visible}

        sx, sy = self.position

        for entity in entities:
            if entity is self or not entity.active:
                continue

            ex, ey = entity.position
            dist: float = math.hypot(ex - sx, ey - sy)
            if dist > self.vision_range:
                continue

            # --- проверяем, нет ли твёрдых объектов на линии взгляда ---
            blocked: bool = False
            for obstacle in entities:
                if (
                    not obstacle.is_solid
                    or obstacle is self
                    or obstacle is entity
                    or not obstacle.active
                ):
                    continue
                if self._segment_intersects_shape(
                    (sx, sy),
                    (ex, ey),
                    obstacle.shape,
                ):
                    blocked = True
                    break

            if not blocked:
                visible.append(entity)

            # # (при необходимости добавить обработку слуха)
            # if dist <= self.hearing_range:
            #     audible.append(entity)

        return {'visible': visible}

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
        Двигается к `target`, пытаясь «скользить» вдоль препятствий.
        1) Пытаемся сделать полный шаг (dx, dy).
        2) Если не получилось — пробуем отдельно по главной оси (X или Y),
           затем по второстепенной.
        3) Угол поворота меняем **только**, если фактически сдвинулись.
        """
        if delta_time == 0.0:
            return

        tx, ty = target
        x,  y  = self.position
        dx, dy = tx - x, ty - y
        dist   = math.hypot(dx, dy)

        if dist == 0.0:
            self._velocity.update(0.0, 0.0)
            return

        # на сколько можем продвинуться за кадр
        step: float = min(self.speed * delta_time, dist)

        # упорядочиваем оси: первой идёт та, где смещение больше
        primary_x_first: bool = abs(dx) >= abs(dy)
        axes: List[Tuple[float, float]] = []

        # полный вектор
        axes.append((dx, dy))
        # движение только по главной оси
        if primary_x_first:
            axes.append((dx, 0.0))
            axes.append((0.0, dy))
        else:
            axes.append((0.0, dy))
            axes.append((dx, 0.0))

        moved: bool = False
        for ax, ay in axes:
            if ax == 0.0 and ay == 0.0:
                continue
            adist = math.hypot(ax, ay)
            nx, ny = ax / adist, ay / adist  # нормализовано
            vx, vy = nx * step / delta_time, ny * step / delta_time
            next_pos: Tuple[float, float] = (x + vx * delta_time, y + vy * delta_time)

            if self._entity_manager.can_move(self, next_pos):
                self._velocity.update(vx, vy)
                self._apply_movement(delta_time)
                self.angle = math.atan2(vy, vx)  # поворачиваемся лишь если двинулись
                moved = True
                break

        if not moved:
            # все варианты заблокированы
            self._velocity.update(0.0, 0.0)

    def render(self, surface: Any) -> None:
        """
        Отрисовать NPC на экране с учётом его текущего угла поворота.
        """
        super().render(surface)  # hit-box / debug-отрисовка из Character

        picture = self._picture_alive if self.is_alive else self._picture_dead

        # поворачиваем картинку на угол (в градусах, по часовой стрелке)
        rotated = pygame.transform.rotate(picture, -math.degrees(self.angle))
        rect = rotated.get_rect(center=self.position)


        #for t in self._route:
        #    pygame.draw.circle(surface, (255, 0, 0), t, 5)


        surface.blit(rotated, rect)

        # ---------- шкала здоровья ----------
        if self.is_alive:
            hp_pct: float = max(0.0, min(1.0, self.health / self.max_health))
            bar_w: int = rect.width
            bar_h: int = 6
            bar_x: int = rect.left
            bar_y: int = rect.top - bar_h - 2

            # цвет: зелёный (100 %) → красный (0 %)
            red: int = int(255 * (1.0 - hp_pct))
            green: int = int(255 * hp_pct)

            # рамка
            pygame.draw.rect(surface, (0, 0, 0),
                             pygame.Rect(bar_x - 1, bar_y - 1, bar_w + 2, bar_h + 2))

            # заполнение
            pygame.draw.rect(surface, (red, green, 0),
                             pygame.Rect(bar_x, bar_y, int(bar_w * hp_pct), bar_h))
