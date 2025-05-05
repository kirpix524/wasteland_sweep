from pathlib import Path
from typing import Tuple
import src.settings as settings

class LevelFileManager:
    """
    Утилитный класс для получения путей к файлам уровня и фона по его номеру.
    Значения берутся из констант settings: LEVEL_{n}_FILE и LEVEL_{n}_BG.
    """

    @staticmethod
    def get_level_file_path(level: int) -> Path:
        """
        Возвращает путь к файлу данных уровня.

        :param level: номер уровня (1, 2, ...)
        :raises ValueError: если константа не найдена в settings
        """
        key = f"LEVEL_{level}_FILE"
        try:
            value = getattr(settings, key)
        except AttributeError:
            raise ValueError(f"Константа '{key}' не найдена в настройках")
        return Path(value)

    @staticmethod
    def get_level_bg_path(level: int) -> Path:
        """
        Возвращает путь к файлу фона уровня.

        :param level: номер уровня (1, 2, ...)
        :raises ValueError: если константа не найдена в settings
        """
        key = f"LEVEL_{level}_BG"
        try:
            value = getattr(settings, key)
        except AttributeError:
            raise ValueError(f"Константа '{key}' не найдена в настройках")
        return Path(value)

    @classmethod
    def get_paths(cls, level: int) -> Tuple[Path, Path]:
        """
        Возвращает кортеж (path_to_level_file, path_to_level_bg).
        """
        return (
            cls.get_level_file_path(level),
            cls.get_level_bg_path(level)
        )
