from typing import List, Optional, Any, Callable

import pygame

from src.entities.modifier import Modifier
from src.entities.character import Character
from src.entities.item import Item
from src.entities.entity import Shape
from src.entities.projectile import Projectile
from src.game.animation import Animation
from src.entities.weapon import Weapon
from src.game.entity_manager import EntityManager


class Player(Character):
    """
    Игрок — живой персонаж с инвентарём, экипированным оружием и бронёй.
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
        angle: float = 0.0,
        picture: Optional[Any] = None,
        animation: Optional[Animation] = None,
        shape: Optional[Shape] = None
    ) -> None:
        print(f"01 picture: {picture}")
        super().__init__(
            entity_manager, entity_id, x, y,
            health, max_health,
            speed, attack, defense,
            vision_range, hearing_range,
            angle, False, True,picture, animation, shape
        )
        print(f"02 picture: {self.picture}")
        # Инвентарь игрока
        self._inventory: List[Item] = []
        # Экипированное оружие и броня
        self._equipped_weapon: Optional[Weapon] = None
        self._equipped_armor:  Optional[Item]   = None
        self.on_shoot: List[Callable[[Projectile], None]] = []

    @property
    def velocity(self) -> pygame.Vector2:
        return self._velocity

    @velocity.setter
    def velocity(self, value: pygame.Vector2) -> None:
        self._velocity = value


    @property
    def inventory(self) -> List[Item]:
        """Список предметов в инвентаре."""
        return self._inventory

    @property
    def equipped_weapon(self) -> Optional[Weapon]:
        """Текущее оружие, которым пользуется игрок."""
        return self._equipped_weapon

    @property
    def equipped_armor(self) -> Optional[Item]:
        """Текущая броня, которую носит игрок."""
        return self._equipped_armor

    def add_to_inventory(self, item: Item) -> None:
        """Добавить предмет в инвентарь: если stackable и есть в инвентаре, увеличить количество."""
        if item.stackable:
            for inv_item in self._inventory:
                if type(inv_item) is type(item) and inv_item.name == item.name:
                    inv_item.quantity += item.quantity
                    return
        self._inventory.append(item)
        if isinstance(item, Weapon):
            self.equip_weapon(item)

    def remove_from_inventory(self, item: Item) -> None:
        """Удалить предмет из инвентаря."""
        self._inventory.remove(item)

    def equip_weapon(self, weapon: Weapon) -> None:
        """
        Экипировать оружие:
        – добавляет его атаку в модификаторы персонажа
        – снимает предыдущую экипировку
        """
        if weapon not in self._inventory:
            raise ValueError("Оружие должно находиться в инвентаре")
        # Снять старое оружие и его модификаторы
        if self._equipped_weapon:
            old = self._equipped_weapon
            # Удаляем все модификаторы атаки, связанные со старым оружием
            for mod in list(self._attack_modifiers):
                if mod.source is old:
                    self.remove_attack_modifier(mod)
        # Экипируем новое оружие
        self._equipped_weapon = weapon
        # Добавляем модификатор атаки от нового оружия
        self.add_attack_modifier(Modifier(weapon.attack_power, weapon))

    def equip_armor(self, armor: Item, defense_bonus: float) -> None:
        """
        Экипировать броню:
        – снимает предыдущую экипировку и удаляет её модификаторы
        – задаёт новую броню
        – добавляет модификатор защиты от новой брони
        """
        if armor not in self._inventory:
            raise ValueError("Броня должна находиться в инвентаре")
        # Снять старую броню и её модификаторы
        if self._equipped_armor:
            old = self._equipped_armor
            for mod in list(self._defense_modifiers):
                if mod.source is old:
                    self.remove_defense_modifier(mod)
        # Экипировать новую броню
        self._equipped_armor = armor
        # Добавить модификатор защиты от брони
        self.add_defense_modifier(Modifier(defense_bonus, armor))

    def fire_bullet(self, target: pygame.Vector2) -> None:
        if self._equipped_weapon is not None:
            if self._equipped_weapon.can_fire():
                bullet = self._equipped_weapon.fire(self.position, target)
                for callback in self.on_shoot:
                    callback(bullet)

    def reload_weapon(self) -> None:
        if self._equipped_weapon is not None:
            self._equipped_weapon.start_reload(None)

    def update(self, delta_time: float) -> None:
        """
        Обновление логики игрока:
        – движение (позиция обновляется в Base/Character.update на основе velocity)
        – проверка столкновений
        – обновление статус-эффектов
        """
        super().update(delta_time)
        if self._equipped_weapon is not None:
            self._equipped_weapon.update(delta_time)

    def render(self, surface: pygame.Surface) -> None:
        """
        Отрисовка игрока на экране с учётом текущего угла поворота ``angle``.
        Поворот выполняется вокруг центра спрайта.
        """
        # Вызываем базовый render (например, для хитбокса или дополнительных эффектов)
        super().render(surface)
        # Определяем, какой спрайт рисовать: кадр анимации или статичную картинку
        sprite: Optional[pygame.Surface] = (
            #self._animation.get_image() if self._animation is not None else self._picture
            self.picture
        )

        if sprite is not None:
            # В pygame положительные углы — против часовой стрелки, поэтому берём «-angle»
            rotated_sprite: pygame.Surface = pygame.transform.rotate(sprite, -self.angle)
            rect: pygame.Rect = rotated_sprite.get_rect(center=(self.position[0], self.position[1]))
            surface.blit(rotated_sprite, rect.topleft)

class PlayerController:
    def __init__(self, player: 'Player') -> None:
        self._player: 'Player' = player
        self._move_x: int = 0
        self._move_y: int = 0
        self._aim_direction: pygame.Vector2 = pygame.Vector2()

    @property
    def player(self) -> 'Player':
        return self._player

    @property
    def position(self) -> pygame.Vector2:
        """Текущее положение центра игрока в мировых координатах."""
        return pygame.Vector2(self.player.position[0], self.player.position[1])

    @property
    def aim_direction(self) -> pygame.Vector2:
        """Нормализованный вектор направления прицеливания."""
        return self._aim_direction

    def _update_velocity(self) -> None:
        """
        Обновляет скорость игрока по направлению (_move_x, _move_y), нормализуя вектор.
        """
        dx: int = self._move_x
        dy: int = self._move_y
        if dx == 0 and dy == 0:
            self._player.velocity.x = 0
            self._player.velocity.y = 0
        else:
            magnitude: float = (dx * dx + dy * dy) ** 0.5
            self._player.velocity.x = dx / magnitude * self._player.speed
            self._player.velocity.y = dy / magnitude * self._player.speed

    def start_move_left(self) -> None:
        self._move_x = -1
        self._update_velocity()

    def start_move_right(self) -> None:
        self._move_x = 1
        self._update_velocity()

    def stop_move_horizontal(self) -> None:
        self._move_x = 0
        self._update_velocity()

    def start_move_up(self) -> None:
        self._move_y = -1
        self._update_velocity()

    def start_move_down(self) -> None:
        self._move_y = 1
        self._update_velocity()

    def stop_move_vertical(self) -> None:
        self._move_y = 0
        self._update_velocity()

    def shoot(self, target: pygame.Vector2) -> None:
        """
        Стреляет по позиции мыши, если оружие экипировано.
        """
        self.update_aim(target)
        self._player.fire_bullet(self.aim_direction)

    def reload(self) -> None:
        """
        Перезарядка текущего оружия.
        """
        self._player.reload_weapon()

    def update_aim(self, target: pygame.Vector2) -> None:
        """
        Обновляет угол поворота игрока в направлении курсора.
        """
        dx: float = target.x - self._player.position[0]
        dy: float = target.y - self._player.position[1]
        self._player.angle = -pygame.Vector2(dx, dy).angle_to(pygame.Vector2(1, 0))

        direction: pygame.Vector2 = target - self.position
        if direction.length_squared() > 0:
            self._aim_direction = direction.normalize()

