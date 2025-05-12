from src.game.entity_factory import EntityFactory
from src.game.level import Level
from src.game.level_manager import LevelManager

from src.settings import LEVEL_PATHS

class GameSession:
    """
    Хранит контекст текущей игры: менеджер уровней, загруженные сущности,
    статистику (очки, жизни), и т. д.
    """
    def __init__(self, entity_factory: 'EntityFactory'):
        self._level_manager: LevelManager = LevelManager(LEVEL_PATHS)
        self._entity_factory: EntityFactory = entity_factory
        self._current_level = None   # тут будем хранить загруженный Level

    @property
    def level_manager(self) -> LevelManager:
        return self._level_manager

    @property
    def current_level(self) -> 'Level':
        return self._current_level

    def start_level(self, level_num: int):
        # загружаем данные уровня (карта, враги и т.д.)
        self._current_level = self.level_manager.load_level(level_num, self._entity_factory)
        # чистим/инициализируем сущности (игрока, врагов, мусор и пр.)
        return self._current_level

    def save(self):
        # сохраняем текущую сессию
        pass

    def _initialize_entities(self):
        # создаём Player, врагов, объекты уровня и т.п.
        # сбрасываем здоровье, позиции и т.д.
        pass
