from abc import ABC
from typing import Any, Optional

from src.entities.character import Character
from src.entities.entity import Entity, Shape
from src.game.entity_manager import EntityManager


class Item(Entity, ABC):
    """
    Базовый класс для предметов, которые можно подбирать.
    """

    def __init__(
        self,
        entity_manager: EntityManager,
        entity_id: int,
        x: float,
        y: float,
        name: str,
        description: str,
        picture: Optional[Any] = None,
        shape: Optional[Shape] = None,
        stackable: bool = False,
        quantity: int = 1
    ) -> None:
        # У предметов всегда collectable = True
        super().__init__(
            entity_manager=entity_manager,
            entity_id=entity_id,
            x=x,
            y=y,
            angle=0.0,
            collectable=True,
            picture=picture,
            shape=shape
        )
        self._name: str = name
        self._description: str = description
        self._stackable: bool = stackable
        self._quantity: int = quantity

    @property
    def name(self) -> str:
        """Название предмета."""
        return self._name

    @property
    def description(self) -> str:
        """Описание предмета."""
        return self._description

    @property
    def stackable(self) -> bool:
        """Можно ли складывать предмет в стак."""
        return self._stackable

    @property
    def quantity(self) -> int:
        """Текущее количество предметов в стеке."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        self._quantity = max(0, value)

    def on_collect(self, collector: Character) -> None:
        """
        Вызывается при сборе предмета.
        По умолчанию добавляет себя в инвентарь collector, если есть.
        """
        if hasattr(collector, 'inventory'):
            collector.inventory.add(self)
        # После сбора можно отключить или удалить предмет из мира
        self.active = False

    def update(self, delta_time: float) -> None:
        """
        Обновление логики предмета (обычно нет необходимости).
        """
        pass

    def render(self, surface: Any) -> None:
        """
        Отрисовка предмета на поверхности.
        """
        if self.picture:
            # предполагаем, что picture — pygame.Surface
            surface.blit(self.picture, self.position)
