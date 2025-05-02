from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.level import Level

class LevelManager:
    def __init__(self, level_paths: List[str]) -> None:
        self._level_paths: List[str] = level_paths
        self._current_index: int = -1
        self._current_level: 'Level' | None = None

    @property
    def current_level(self) -> 'Level':
        if self._current_level is None:
            raise RuntimeError("No level loaded")
        return self._current_level

    @property
    def current_level_number(self) -> int:
        if self._current_index < 0:
            raise RuntimeError("No level loaded")
        return self._current_index + 1

    @property
    def level_count(self) -> int:
        return len(self._level_paths)

    def load_level(self, level_number: int) -> 'Level':
        if level_number < 1 or level_number > len(self._level_paths):
            raise ValueError(f"Level number {level_number} out of range")
        self._current_index = level_number - 1
        path: str = self._level_paths[self._current_index]
        self._current_level = Level.load_from_file(path)
        return self._current_level

    def has_next_level(self) -> bool:
        return self._current_index + 1 < len(self._level_paths)

    def load_next_level(self) -> 'Level':
        if not self.has_next_level():
            raise RuntimeError("No next level available")
        return self.load_level(self._current_index + 2)


