"""Contains stuff for versions."""


from __future__ import annotations

from .. import m_handlers, m_level_data
from . import m_combine_settings, m_branches


class PAVersion(m_handlers.JSONClassHandler):
    """Represents a PA version."""
    version_number: str
    branch: type[m_branches.Branch]

    _all_versions: list[type[PAVersion]] = []


    def __init_subclass__(cls) -> None:
        cls._all_versions.append(cls)


    @classmethod
    def to_json(cls):
        return {
            "version_number": cls.version_number
        }

    @classmethod
    def _from_json_unwrap(cls, json_data: dict | list):
        return cls.get_version_from_number(json_data["version_number"])


    @classmethod
    def get_description(cls):
        """Gets the description of this version."""
        return f"v{cls.version_number} ({cls.branch.name.capitalize()} branch)"

    @classmethod
    def get_all_versions(cls):
        """Gets all supported PA versions."""
        return cls._all_versions

    @classmethod
    def get_version_from_number(cls, version_number: str):
        """Gets the version from a version number."""
        for version in cls.get_all_versions():
            if version.version_number == version_number:
                return version

        raise ValueError("Version not found or not supported.")

    @classmethod
    def get_version_from_description(cls, description: str):
        """Gets the version from its description."""
        for version in cls.get_all_versions():
            if version.get_description() == description:
                return version

        raise ValueError("Version not found or not supported.")


    @classmethod
    def get_version_number(cls, level: m_level_data.Level):
        """Gets the version number of the level."""

    @classmethod
    def is_compatible_level(cls, level: m_level_data.Level):
        """Returns `True` if the level is compatible with this version, otherwise `False`."""


    @classmethod
    def import_level_folder(cls, level_folder: str, load_audio: bool = True) -> m_level_data.LevelFolder:
        """Gets the level data from a folder."""

    @classmethod
    def export_level_folder(cls, level_folder: m_level_data.LevelFolder, folder_path: str):
        """Exports the level folder."""


    @classmethod
    def get_custom_themes_from_level(cls, level: m_level_data.Level, themes_folder_path: str) -> list[m_level_data.Theme]:
        """Gets the themes from the level to a folder."""

    @classmethod
    def get_theme_ids_from_level(cls, level: m_level_data.Level):
        """Returns all theme IDs used in all theme keyframes of the level."""

    @classmethod
    def get_theme_from_id(cls, themes_folder_path: str, theme_id: int) -> m_level_data.Theme:
        """Gets the theme containing the ID in the themes folder."""

    @classmethod
    def get_all_themes_in_folder(cls, themes_folder_path: str) -> list[m_level_data.Theme]:
        """Returns all themes in a folder."""


    default_checkpoint: dict
    default_event_kfs: dict[str, list]


    @classmethod
    def combine_levels(
            cls,
            levels: list[m_level_data.Level],
            primary_level: m_level_data.Level = None,
            combine_settings: m_combine_settings.CombineSettings = m_combine_settings.CombineSettings()
        ):
        """
        Combines levels to one file with the provided combine settings.
        If provided, the primary level will be combined to the other levels and will keep all properties regardless of the combine settings.
        """
