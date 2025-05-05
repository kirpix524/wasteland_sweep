from typing import Type, Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.entity import Entity

class EntityFactory:
    def __init__(self) -> None:
        # Регистрация ключ->класс сущности
        self._registry: Dict[str, Type['Entity']] = {}

    def register(self, key: str, entity_cls: Type['Entity']) -> None:
        """
        Регистрирует класс сущности под указанным ключом.

        :param key: Уникальный идентификатор типа сущности
        :param entity_cls: класс, наследник Entity
        :raises KeyError: если ключ уже зарегистрирован
        """
        if key in self._registry:
            raise KeyError(f"Entity key '{key}' already registered")
        self._registry[key] = entity_cls

    def create(self, key: str, *args: Any, **kwargs: Any) -> 'Entity':
        """
        Создаёт экземпляр сущности по ключу и передаёт все аргументы в конструктор.

        :param key: Ключ зарегистрированного типа сущности
        :param args: позиционные аргументы для конструктора
        :param kwargs: именованные аргументы для конструктора
        :return: экземпляр сущности
        :raises KeyError: если ключ не зарегистрирован
        """
        if key not in self._registry:
            raise KeyError(f"Entity key '{key}' is not registered")
        cls = self._registry[key]
        entity = cls(*args, **kwargs)
        return entity

    @property
    def registered_keys(self) -> List[str]:
        """
        Список всех зарегистрированных ключей сущностей.
        """
        return list(self._registry.keys())