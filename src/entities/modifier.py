from src.entities.entity import Entity

class Modifier:
    """
    Описывает изменение характеристики:
    - value: величина бонуса/штрафа
    - source: сущность, вызвавшая модификатор
    """
    def __init__(self, value: float, source: Entity) -> None:
        self._value: float = value
        self._source: Entity = source

    @property
    def value(self) -> float:
        return self._value

    @property
    def source(self) -> Entity:
        return self._source
