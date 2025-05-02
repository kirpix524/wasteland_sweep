from typing import List, Optional, Any
from modifier import Modifier
from character import Character
from item import Item
from src.entities.entity import Shape
from src.game.animation import Animation
from weapon import Weapon

class Player(Character):
    """
    Игрок — живой персонаж с инвентарём, экипированным оружием и бронёй.
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
        angle: float = 0.0,
        picture: Optional[Any] = None,
        animation: Optional[Animation] = None,
        shape: Optional[Shape] = None
    ) -> None:
        super().__init__(
            entity_id, x, y,
            health, max_health,
            speed, attack, defense,
            vision_range, hearing_range,
            angle, False, picture, animation, shape
        )
        # Инвентарь игрока
        self._inventory: List[Item] = []
        # Экипированное оружие и броня
        self._equipped_weapon: Optional[Weapon] = None
        self._equipped_armor:  Optional[Item]   = None

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

    def update(self, delta_time: float) -> None:
        """
        Обновление логики игрока:
        – ввод/движение
        – проверка столкновений
        – обновление эффектов
        """
        super().update(delta_time)
        # TODO: реализовать логику управления игроком

    def render(self, surface: Any) -> None:
        """
        Отрисовка игрока на экране.
        """
        super().render(surface)
        # TODO: отрисовать HUD и прицел
