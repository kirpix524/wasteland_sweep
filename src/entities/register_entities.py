from src.game.entity_factory import EntityFactory
from src.entities.player import Player

def register_entities(entity_manager: 'EntityFactory') -> None:
    entity_manager.register('player', Player)
