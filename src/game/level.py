from typing import List, Tuple, Optional, Any

import pygame

from src.entities.character import Character
from src.entities.entity import Entity, CircleShape, RectangleShape
from src.entities.item import Item
from src.entities.map_entity import MapEntity
from src.entities.npc import NPC, Attitude, ZombieDecisionModule
from src.entities.player import PlayerController, Player
from src.entities.weapon import Weapon, FireMode
from src.game.entity_factory import EntityFactory
from src.game.entity_manager import EntityManager
from src.settings import (PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT,
                          AK_IMAGE, AK_WIDTH, AK_HEIGHT, AK_SOUND,
                          MINIGUN_IMAGE, MINIGUN_WIDTH, MINIGUN_HEIGHT, MINIGUN_SOUND,
                          DEAD_TANK_IMAGE, DEAD_TANK_WIDTH, DEAD_TANK_HEIGHT,
                          ZOMBIE_1_ALIVE_IMAGE, ZOMBIE_1_DEAD_IMAGE, ZOMBIE_1_WIDTH, ZOMBIE_1_HEIGHT, SCREEN_WIDTH,
                          ZOMBIE_2_ALIVE_IMAGE, ZOMBIE_2_DEAD_IMAGE, ZOMBIE_2_WIDTH, ZOMBIE_2_HEIGHT,
                          ZOMBIE_DOG_1_ALIVE_IMAGE, ZOMBIE_DOG_1_DEAD_IMAGE, ZOMBIE_DOG_1_WIDTH, ZOMBIE_DOG_1_HEIGHT,
                          ROBOT_1_ALIVE_IMAGE, ROBOT_1_DEAD_IMAGE, ROBOT_1_WIDTH, ROBOT_1_HEIGHT,
                          SCREEN_HEIGHT)
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
        level_num: int,
        name: str,
        briefing_message: str,
        level_complete_message: str,
        entity_factory: EntityFactory,
        player_controller: Optional[PlayerController] = None,
        background: Optional[Any] = None,
        music: Optional[str] = None
    ) -> None:
        # Идентификатор уровня (только для чтения)
        self._id: str = level_id
        self._level_num: int = level_num
        # Название уровня
        self._name: str = name
        self._briefing_message: str = briefing_message
        self._level_complete_message: str = level_complete_message
        # Фоновые настройки: изображение, анимация
        self._background: Optional[Any] = background
        # Фоновая музыка для уровня
        self._music: Optional[str] = music
        self._entity_manager: EntityManager = EntityManager(entity_factory)
        self._player_controller: Optional[PlayerController] = player_controller
        self._is_completed: bool = False

    @property
    def is_completed(self) -> bool:
        return self._is_completed

    @property
    def briefing_message(self) -> str:
        return self._briefing_message

    @property
    def level_complete_message(self) -> str:
        return self._level_complete_message

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
    def level_num(self) -> int:
        return self._level_num

    @property
    def name(self) -> str:
        return self._name

    @property
    def entities(self) -> List[Entity]:
        return self._entity_manager.all_entities

    @property
    def background(self) -> Optional[Any]:
        return self._background

    @property
    def music(self) -> Optional[str]:
        return self._music

    def add_entity(self, entity: Entity) -> None:
        """Добавить игровую сущность на уровень."""
        self.entity_manager.add_existing_entity(entity)

    def remove_entity(self, entity: Entity) -> None:
        """Удалить игровую сущность с уровня."""
        self.entity_manager.remove_entity_by_id(entity.id)

    def get_entities_in_area(self, area: Tuple[int, int, int, int]) -> List[Entity]:
        """Вернуть список сущностей в заданной прямоугольной зоне (x, y, w, h)."""
        x, y, w, h = area
        result: List[Entity] = []
        for e in self.entities:
            ex, ey = e.position
            if x <= ex <= x + w and y <= ey <= y + h:
                result.append(e)
        return result

    def update(self, delta_time: float) -> None:
        """Обновить все сущности и триггеры на уровне."""
        is_completed = True
        for e in list(self.entities):
            e.update(delta_time)
            if isinstance(e, NPC):
                if (e.attitude==Attitude.HOSTILE) and e.is_alive:
                    is_completed = False
        self._is_completed = is_completed
        self._check_item_pickup()

    def _check_item_pickup(self) -> None:
        """Проверить, подобрал ли игрок предметы, и обработать сбор."""
        if self._player_controller is None:
            return

        player: Entity = self._player_controller.player
        for item in [e for e in self.entities if isinstance(e, Item)]:
            if player.collides_with(item):
                if not item.collectable or not item.active:
                    continue
                if hasattr(self._player_controller.player, "add_to_inventory"):
                    self._player_controller.player.add_to_inventory(item)
                self.remove_entity(item)

    def render(self, surface: Any) -> None:
        """Отрисовать тайл-карту, фон и все сущности."""
        # Рисуем фон
        if self._background:
            surface.blit(self._background, (0, 0))
        # Рисуем сущности
        for e in self.entities:
            if isinstance(e, Character):
                if e.is_alive:
                    continue
            e.render(surface)
        for e in self.entities:
            if isinstance(e, Character):
                if not e.is_alive:
                    continue
            e.render(surface)

    def get_picture(self, path: str, width: int, height: int) -> pygame.image:
        picture = pygame.image.load(path).convert_alpha()
        picture = pygame.transform.scale(picture, (width, height))
        return picture

    @classmethod
    def load_from_file(cls, path: str, level_num: int, entity_factory: EntityFactory) -> 'Level':
        """Загрузить уровень из JSON/YAML-файла."""
        # Реализация загрузчика (Parser + фабрики сущностей)
        level_id="level_"+str(level_num)
        level_name="Test level"
        briefing_message="Убей всех врагов"
        level_complete_message="Уровень пройден"
        level_bg_path = LevelFileManager.get_level_bg_path(1)
        level_bg=pygame.image.load(level_bg_path).convert()
        level_bg = pygame.transform.scale(level_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        level = Level(level_id=level_id,
                      level_num=level_num,
                      name=level_name,
                      briefing_message=briefing_message,
                      level_complete_message=level_complete_message,
                      entity_factory=entity_factory,
                      background=level_bg)
        player_image = level.get_picture(PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT)
        player = Player(level.entity_manager,
                        0,
                        1000,
                        300,
                        300,
                        300,
                        150,
                        10,
                        10,
                        300,
                        0,
                        picture=player_image,
                        shape=CircleShape(300, 300, 25))

        ak_picture = level.get_picture(AK_IMAGE, AK_WIDTH, AK_HEIGHT)
        ak47 = Weapon(level.entity_manager,
                      0,
                      1200,
                      300,
                      "ak-47",
                      "ak-47 rifle",
                      2000,
                      800,
                      150,
                      3,
                      500,
                      300,
                      30,
                      ak_picture,
                      [FireMode.SINGLE, FireMode.AUTO],
                      10,
                      RectangleShape(600, 300, AK_WIDTH, AK_HEIGHT),
                      fire_sound=AK_SOUND)
        level.entity_manager.add_existing_entity(ak47)

        minigun_picture = level.get_picture(MINIGUN_IMAGE, int(MINIGUN_WIDTH*1.2), int(MINIGUN_HEIGHT*1.2))
        minigun = Weapon(level.entity_manager,
                         0,
                         1200,
                         500,
                         "minigun",
                         "big fucking gun",
                         3000,
                         1000,
                         250,
                         8,
                         700,
                         400,
                         500,
                         minigun_picture,
                         [FireMode.AUTO],
                         30,
                         RectangleShape(600, 500, MINIGUN_WIDTH, MINIGUN_HEIGHT),
                         fire_sound=MINIGUN_SOUND)
        level.entity_manager.add_existing_entity(minigun)

        tank_picture = level.get_picture(DEAD_TANK_IMAGE, int(DEAD_TANK_WIDTH*1.2), int(DEAD_TANK_HEIGHT*1.2))
        tank = MapEntity(level.entity_manager,
                        0,
                        800,
                        700,
                        100,
                        tank_picture,
                        RectangleShape(800, 700, DEAD_TANK_WIDTH, DEAD_TANK_HEIGHT))
        #level.entity_manager.add_existing_entity(tank)

        zombie_alive_picture = level.get_picture(ZOMBIE_1_ALIVE_IMAGE, ZOMBIE_1_WIDTH, ZOMBIE_1_HEIGHT)
        zombie_dead_picture = level.get_picture(ZOMBIE_1_DEAD_IMAGE, ZOMBIE_1_WIDTH, ZOMBIE_1_HEIGHT)

        for i in range(5):
            for j in range(5):
                zombie = NPC(level.entity_manager,
                     0,
                     100+i*100,
                     600+j*100,
                     1000,
                     1000,
                     20,
                     20,
                     50,
                     3000,
                     "zombie",
                     Attitude.HOSTILE,
                     ZombieDecisionModule(),
                     picture_alive=zombie_alive_picture,
                     picture_dead=zombie_dead_picture,
                     shape=CircleShape(200, 800, 25))
                level.entity_manager.add_existing_entity(zombie)

        zombie_dog_alive_picture = level.get_picture(ZOMBIE_DOG_1_ALIVE_IMAGE, ZOMBIE_DOG_1_WIDTH, ZOMBIE_DOG_1_HEIGHT)
        zombie_dog_dead_picture = level.get_picture(ZOMBIE_DOG_1_DEAD_IMAGE, ZOMBIE_DOG_1_WIDTH, ZOMBIE_DOG_1_HEIGHT)

        for i in range(5):
            zombie_dog = NPC(level.entity_manager,
                     0,
                     100+i*100,
                     300,
                     500,
                     500,
                     120,
                     25,
                     30,
                     3000,
                     "zombie dog",
                     Attitude.HOSTILE,
                     ZombieDecisionModule(),
                     picture_alive=zombie_dog_alive_picture,
                     picture_dead=zombie_dog_dead_picture,
                     shape=RectangleShape(200, 800, 30, 45))
            level.entity_manager.add_existing_entity(zombie_dog)

        for i in range(5):
            robot_alive_picture = level.get_picture(ROBOT_1_ALIVE_IMAGE, ROBOT_1_WIDTH, ROBOT_1_HEIGHT)
            robot_dead_picture = level.get_picture(ROBOT_1_DEAD_IMAGE, ROBOT_1_WIDTH, ROBOT_1_HEIGHT)
            robot = NPC(level.entity_manager,
                     0,
                     900+i*100,
                        1100,
                        5000,
                        5000,
                        100,
                        60,
                        90,
                        3000,
                        "robot",
                        Attitude.HOSTILE,
                        ZombieDecisionModule(),
                        picture_alive=robot_alive_picture,
                        picture_dead=robot_dead_picture,
                        shape=CircleShape(200, 800, 30))
            level.entity_manager.add_existing_entity(robot)

        level.entity_manager.add_existing_entity(player)
        player_controller = PlayerController(player)
        level._player_controller = player_controller

        return level

    def save_to_file(self, path: str) -> None:
        """Сохранить текущее состояние уровня в файл."""
        ...
