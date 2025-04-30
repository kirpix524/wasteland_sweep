classDiagram
    GameManager "1" -- "*" System
    GameManager o-- EntityManager
    GameManager o-- Map

    EntityManager "1" -- "*" Entity

    %% Entities
    class Entity {
      - id: int
      - components: dict
      + add_component(c: Component)
      + get_component(type) -> Component
    }
    class Player
    class Enemy
    class Drone
    class Projectile
    class ItemPickup

    Entity <|-- Player
    Entity <|-- Enemy
    Entity <|-- Drone
    Entity <|-- Projectile
    Entity <|-- ItemPickup

    %% Components
    class PositionComponent
    class VelocityComponent
    class RenderComponent
    class HealthComponent
    class InputComponent
    class AIComponent
    class WeaponComponent
    class LightComponent
    class InventoryComponent
    class CollectibleComponent

    Component <|-- PositionComponent
    Component <|-- VelocityComponent
    Component <|-- RenderComponent
    Component <|-- HealthComponent
    Component <|-- InputComponent
    Component <|-- AIComponent
    Component <|-- WeaponComponent
    Component <|-- LightComponent
    Component <|-- InventoryComponent
    Component <|-- CollectibleComponent

    %% Systems
    class System {
      + update(dt: float)
    }
    class MovementSystem
    class RenderSystem
    class CollisionSystem
    class InputSystem
    class AISystem
    class WeaponSystem
    class LightSystem
    class CollectionSystem

    System <|-- MovementSystem
    System <|-- RenderSystem
    System <|-- CollisionSystem
    System <|-- InputSystem
    System <|-- AISystem
    System <|-- WeaponSystem
    System <|-- LightSystem
    System <|-- CollectionSystem
