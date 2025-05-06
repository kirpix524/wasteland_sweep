from abc import ABC, abstractmethod
from typing import Tuple, Any, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from src.game.entity_manager import EntityManager


class Shape(ABC):
    """
    Абстрактный класс для формы объекта.
    Прописывает методы для получения ограничивающего прямоугольника и проверки пересечения.
    """

    @abstractmethod
    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Возвращает ограничивающий прямоугольник (x, y, width, height).
        """
        ...

    @abstractmethod
    def intersects(self, other: 'Shape') -> bool:
        """
        Проверяет пересечение этой формы с другой.
        """
        ...


class RectangleShape(Shape):
    """
    Прямоугольная форма объекта.
    Поддерживает проверку пересечений с прямоугольником и кругом.
    """
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self._x: float = x
        self._y: float = y
        self._width: float = width
        self._height: float = height

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value

    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        return (self._x, self._y, self._width, self._height)

    def intersects(self, other: Shape) -> bool:
        if isinstance(other, RectangleShape):
            # AABB пересечение
            return (
                self._x < other.x + other.width and
                self._x + self._width > other.x and
                self._y < other.y + other.height and
                self._y + self._height > other.y
            )
        elif isinstance(other, CircleShape):
            # Ближайшая точка прямоугольника к центру круга
            circle_dist_x = abs(other.center_x - (self._x + self._width / 2))
            circle_dist_y = abs(other.center_y - (self._y + self._height / 2))
            if circle_dist_x > (self._width / 2 + other.radius):
                return False
            if circle_dist_y > (self._height / 2 + other.radius):
                return False
            if circle_dist_x <= (self._width / 2):
                return True
            if circle_dist_y <= (self._height / 2):
                return True
            # Проверка углового пересечения
            corner_dist_sq = (
                circle_dist_x - self._width / 2
            ) ** 2 + (
                circle_dist_y - self._height / 2
            ) ** 2
            return corner_dist_sq <= (other.radius ** 2)
        return False


class CircleShape(Shape):
    """
    Круглая форма объекта.
    Поддерживает проверку пересечения с кругом и прямоугольником.
    """
    def __init__(self, center_x: float, center_y: float, radius: float) -> None:
        self._center_x: float = center_x
        self._center_y: float = center_y
        self._radius: float = radius

    @property
    def center_x(self) -> float:
        return self._center_x

    @center_x.setter
    def center_x(self, value: float) -> None:
        self._center_x = value

    @property
    def center_y(self) -> float:
        return self._center_y

    @center_y.setter
    def center_y(self, value: float) -> None:
        self._center_y = value

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        self._radius = value

    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        x = self._center_x - self._radius
        y = self._center_y - self._radius
        size = self._radius * 2
        return (x, y, size, size)

    def intersects(self, other: Shape) -> bool:
        if isinstance(other, CircleShape):
            # Круг-круг пересечение
            dx = self._center_x - other.center_x
            dy = self._center_y - other.center_y
            distance_sq = dx * dx + dy * dy
            radius_sum = self._radius + other.radius
            return distance_sq <= (radius_sum * radius_sum)
        elif isinstance(other, RectangleShape):
            # Делегируем проверку прямоугольнику
            return other.intersects(self)
        return False


class Entity(ABC):
    """
    Базовый класс для всех игровых объектов.
    Хранит идентификатор, положение, угол поворота, состояние активности,
    возможность сбора, картинку и форму (shape).
    """

    def __init__(
        self,
        entity_manager: 'EntityManager',
        entity_id: int,
        x: float = 0.0,
        y: float = 0.0,
        angle: float = 0.0,
        collectable: bool = False,
        picture: Optional[Any] = None,
        shape: Optional[Shape] = None
    ) -> None:
        self._manager: 'EntityManager' = entity_manager
        self._id: int = entity_id
        self._position: Tuple[float, float] = (x, y)
        self._angle: float = angle
        self._active: bool = True
        self._collectable: bool = collectable
        self._picture: Optional[Any] = picture
        print(f"entity picture: {self.picture}")

        if shape is None:
            self._shape: Shape = RectangleShape(x, y, 0.0, 0.0)
        else:
            self._shape = shape
            # Синхронизируем позицию формы
            if isinstance(self._shape, RectangleShape):
                self._shape.x, self._shape.y = self._position
            elif isinstance(self._shape, CircleShape):
                self._shape.center_x, self._shape.center_y = self._position

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        self._id = value

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @position.setter
    def position(self, value: Tuple[float, float]) -> None:
        self._position = value
        if isinstance(self._shape, RectangleShape):
            self._shape.x, self._shape.y = value
        elif isinstance(self._shape, CircleShape):
            self._shape.center_x, self._shape.center_y = value

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, value: float) -> None:
        self._angle = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

    @property
    def collectable(self) -> bool:
        return self._collectable

    @property
    def picture(self) -> Optional[Any]:
        return self._picture

    @picture.setter
    def picture(self, value: Any) -> None:
        self._picture = value

    @property
    def shape(self) -> Shape:
        return self._shape

    def collides_with(self, other: 'Entity') -> bool:
        """
        Проверяет пересечение формы этого объекта с формой другого объекта.

        :param other: Другая сущность для проверки столкновения
        :return: True, если формы пересекаются
        """
        return self._shape.intersects(other.shape)

    @abstractmethod
    def update(self, delta_time: float) -> None:
        ...

    @abstractmethod
    def render(self, surface: Any) -> None:
        ...
