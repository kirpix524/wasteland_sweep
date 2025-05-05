from typing import List, Tuple, Optional, Any

import pygame

from src.entities.entity import Entity
from src.entities.player import PlayerController, Player
from src.game.entity_factory import EntityFactory
from src.game.entity_manager import EntityManager
from src.settings import PLAYER_IMAGE
from src.utils.level_file_manager import LevelFileManager


class Level:
    """
    Класс для хранения информации об уровне:
      - идентификатор и название
      - сущности
      - музыка и фон
    """
    def __init__(
        self,
        level_id: str,
        name: str,
        entities: List[Entity],
        briefing_message: str,
        entity_factory: EntityFactory,
        player_controller: Optional[PlayerController] = None,
        background: Optional[Any] = None,
        music: Optional[str] = None
    ) -> None:
        # Идентификатор уровня (только для чтения)
        self._id: str = level_id
        # Название уровня
        self._name: str = name
        self._briefing_message: str = briefing_message
        # Все сущности на уровне
        self._entities: List[Entity] = entities
        # Фоновые настройки: изображение, анимация
        self._background: Optional[Any] = background
        # Фоновая музыка для уровня
        self._music: Optional[str] = music
        self._entity_manager: EntityManager = EntityManager(entity_factory)
        self._player_controller: Optional[PlayerController] = player_controller

    @property
    def briefing_message(self) -> str:
        return self._briefing_message

    @property
    def entity_manager(self) -> EntityManager:
        return self._entity_manager

    @property
    def player_controller(self) -> PlayerController:
        return self._player_controller

    @player_controller.setter
    def player_controller(self, player_controller: PlayerController) -> None:
        self._player_controller = player_controller

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def entities(self) -> List[Entity]:
        return list(self._entities)

    @property
    def background(self) -> Optional[Any]:
        return self._background

    @property
    def music(self) -> Optional[str]:
        return self._music

    def add_entity(self, entity: Entity) -> None:
        """Добавить игровую сущность на уровень."""
        self._entities.append(entity)

    def remove_entity(self, entity: Entity) -> None:
        """Удалить игровую сущность с уровня."""
        self._entities.remove(entity)

    def get_entities_in_area(self, area: Tuple[int, int, int, int]) -> List[Entity]:
        """Вернуть список сущностей в заданной прямоугольной зоне (x, y, w, h)."""
        x, y, w, h = area
        result: List[Entity] = []
        for e in self._entities:
            ex, ey = e.position
            if x <= ex <= x + w and y <= ey <= y + h:
                result.append(e)
        return result

    def update(self, delta_time: float) -> None:
        """Обновить все сущности и триггеры на уровне."""
        # Обновление сущностей
        for e in list(self._entities):
            e.update(delta_time)

    def render(self, surface: Any) -> None:
        """Отрисовать тайл-карту, фон и все сущности."""
        # Рисуем фон
        if self._background:
            surface.blit(self._background, (0, 0))
        # Рисуем сущности
        for e in self._entities:
            e.render(surface)

    @classmethod
    def load_from_file(cls, path: str, entity_factory: EntityFactory) -> 'Level':
        """Загрузить уровень из JSON/YAML-файла."""
        # Реализация загрузчика (Parser + фабрики сущностей)
        level_id="level_1"
        level_name="Test level"
        briefing_message="Убей всех врагов"
        level_bg_path = LevelFileManager.get_level_bg_path(1)
        level_bg=pygame.image.load(level_bg_path).convert()
        level = Level(level_id,
                      level_name,
                      [],
                      briefing_message,
                      entity_factory,
                      background=level_bg)
        player_image = pygame.image.load(PLAYER_IMAGE)
        player = Player(0, 100, 100, 100, 100, 50, 10, 10, 300, 150,0, picture=player_image)
        level.entity_manager.add_existing_entity(player)
        player_controller = PlayerController(player)
        level._player_controller = player_controller
        player.on_shoot.append(level.add_entity)
        return level

    def save_to_file(self, path: str) -> None:
        """Сохранить текущее состояние уровня в файл."""
        ...
