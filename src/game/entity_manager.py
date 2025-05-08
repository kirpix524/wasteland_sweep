from typing import Dict, Any, List, Tuple
from src.entities.entity import Entity
from src.game.entity_factory import EntityFactory

class EntityManager:
    def __init__(self, factory: EntityFactory) -> None:
        """
        Менеджер игровых сущностей:
        - хранит созданные сущности
        - выдаёт уникальный id для каждой новой сущности
        """
        self._factory: EntityFactory = factory
        self._entities: Dict[int, Entity] = {}
        self._next_id: int = 1

    def create_entity(self, key: str, *args: Any, **kwargs: Any) -> Entity:
        """
        Создаёт сущность через фабрику, присваивает ей новый id и сохраняет в списке.

        :param key: ключ, зарегистрированный в EntityFactory
        :param args: позиционные аргументы для конструктора сущности
        :param kwargs: именованные аргументы для конструктора сущности
        :return: уникальный идентификатор созданной сущности
        """
        entity_id: int = self._next_id
        self._next_id += 1
        entity: Entity = self._factory.create(key, entity_id=entity_id, *args, **kwargs)
        # Присваиваем id самой сущности (если у неё есть атрибут entity_id)
        self._entities[entity_id] = entity
        return entity

    def add_existing_entity(self, entity: Entity) -> None:
        """
        Добавляет существующую сущность в менеджер.

        :param entity: сущность, которую нужно сохранить
        """
        entity_id: int = self._next_id
        self._next_id += 1
        entity.id = entity_id
        self._entities[entity.id] = entity

    def get_entity_by_id(self, entity_id: int) -> Entity:
        """
        Возвращает сущность по её идентификатору.

        :param entity_id: идентификатор сущности
        :raises KeyError: если сущность не найдена
        """
        try:
            return self._entities[entity_id]
        except KeyError:
            raise KeyError(f"Entity id {entity_id} not found")

    def remove_entity_by_id(self, entity_id: int) -> None:
        """
        Удаляет сущность из менеджера.

        :param entity_id: идентификатор сущности
        :raises KeyError: если сущность не найдена
        """
        if entity_id in self._entities:
            del self._entities[entity_id]
        else:
            raise KeyError(f"Entity id {entity_id} not found")

    @property
    def all_entities(self) -> List[Entity]:
        """
        Возвращает список всех управляющихся сущностей.
        """
        return list(self._entities.values())

    def can_move(self,
                 entity: 'Entity',
                 new_pos: Tuple[float, float]) -> bool:
        """
        Возвращает True, если entity может переместиться в new_pos,
        не столкнувшись с твёрдыми объектами.
        """
        original: Tuple[float, float] = entity.position
        entity.position = new_pos
        try:
            for other in self.all_entities:
                if other is entity or not other.is_solid:
                    continue
                if entity.collides_with(other):
                    return False
            return True
        finally:
            entity.position = original