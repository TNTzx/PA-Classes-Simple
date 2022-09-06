"""Contains the class for level data."""


from __future__ import annotations

from . import m_handlers, m_disk_utils, l_versions, m_level_excs


class LevelData(m_handlers.JSONFileHandler):
    """Represents a certain file in levels."""


class JSONData(LevelData):
    """Level data that contains JSON."""
    def __init__(self, data: dict | list):
        self.data = data


    def to_json(self) -> dict | list:
        return {
            "data": self.data
        }

    @classmethod
    def _from_json_unwrap(cls, json_data: dict | list):
        return cls(
            data = json_data["data"]
        )


class Level(JSONData):
    """Represents a `level.lsb` file."""


class Metadata(JSONData):
    """Represents a `metadata.lsb` file."""


class Audio(LevelData):
    """Represents the audio (`level.ogg`) of a level."""
    def __init__(self, audio_bytes: bytes):
        self.audio_bytes = audio_bytes


    @classmethod
    def from_path(cls, path: str):
        """Gets the audio from a path."""
        if not m_disk_utils.path_exists(path):
            raise m_level_excs.AudioImportException(path)

        return cls(
            audio_bytes = m_disk_utils.read_file(path, binary = True)
        )


    def to_json(self) -> dict | list:
        return {
            "audio_bytes": m_disk_utils.bytes_to_base64(self.audio_bytes)
        }


    @classmethod
    def _from_json_unwrap(cls, json_data: dict | list):
        return cls(
            audio_bytes = m_disk_utils.base64_to_bytes(json_data["audio_bytes"])
        )


class Theme(JSONData):
    """Represents a `.lst` file."""


class LevelFolder(m_handlers.JSONFileHandler):
    """Represents a level folder."""
    def __init__(
            self,
            version: type[l_versions.PAVersion],
            level: Level,
            metadata: Metadata,
            audio: Audio | None,
            themes: list[Theme]
        ):
        self.version = version
        self.level = level
        self.metadata = metadata
        self.audio = audio
        self.themes = themes


    def to_json(self) -> dict | list:
        return {
            "version": self.version.to_json(),
            "level": self.level.to_json(),
            "metadata": self.metadata.to_json(),
            "audio": self.audio.to_json() if self.audio is not None else None,
            "themes": [theme.to_json() for theme in self.themes]
        }

    @classmethod
    def _from_json_unwrap(cls, json_data: dict | list):
        return cls(
            version = l_versions.PAVersion.from_json(json_data["version"]),
            level = Level.from_json(json_data["level"]),
            metadata = Metadata.from_json(json_data["metadata"]),
            audio = Audio.from_json(json_data["audio"]) if json_data["audio"] is not None else None,
            themes = [Theme.from_json(theme_json) for theme_json in json_data["themes"]]
        )


    @classmethod
    def combine_folders(cls, level_folders: list[LevelFolder], primary_level_folder: LevelFolder | None = None, combine_settings: l_versions.CombineSettings = l_versions.CombineSettings()):
        """Combines two level folders into one."""
        source = primary_level_folder if primary_level_folder is not None else level_folders[0]

        levels = [level_folder.level for level_folder in level_folders]
        level = source.version.combine_levels(levels, source.level, combine_settings)

        themes: list[Theme] = []
        for level_folder in level_folders:
            themes += [theme for theme in level_folder.themes if theme not in themes]

        return cls(
            version = source.version,
            level = level,
            metadata = source.metadata,
            audio = source.audio,
            themes = themes
        )
