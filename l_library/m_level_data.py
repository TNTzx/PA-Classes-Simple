"""Contains the class for level data."""


from __future__ import annotations

from . import m_handlers, m_disk_utils, l_versions, m_level_excs


class LevelData(m_handlers.JSONFileHandler, m_handlers.RawFileHandler):
    """Represents a certain file in levels."""


class JSONData(LevelData):
    """Level data that contains JSON."""
    def __init__(self, data: dict | list = None):
        if data is None:
            data = {}
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

    # TEST
    def to_file_raw(self, folder_path: str, filename: str):
        m_disk_utils.override_file(
            folder_path,
            self.append_file_ext_raw(filename),
            str(self.data)
        )

    @classmethod
    def from_file_raw(cls, file_path: str):
        return cls(data = m_disk_utils.read_file(file_path, False))


class Level(JSONData):
    """Represents a `level.lsb` file."""
    raw_file_ext: str = "lsb"


class Metadata(JSONData):
    """Represents a `metadata.lsb` file."""
    raw_file_ext: str = "lsb"


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


    def to_file_raw(self, folder_path: str, filename: str):
        m_disk_utils.override_file(
            folder_path,
            self.append_file_ext(filename),
            self.audio_bytes,
            binary = True
        )

    @classmethod
    def from_file_raw(cls, file_path: str):
        return cls(audio_bytes = m_disk_utils.read_file(file_path, True))


class Theme(JSONData):
    """Represents a `.lst` file."""
    raw_file_ext: str = "lst"


class LevelFolder(m_handlers.JSONHandler):
    """Contains the data for a level folder."""
    def __init__(
            self,
            version: type[l_versions.PAVersion] = l_versions.DEFAULT_VERSION,
            level: Level = Level(),
            metadata: Metadata = Metadata(),
            audio: Audio | None = None
        ):
        self.version = version
        self.level = level
        self.metadata = metadata
        self.audio = audio


    def to_json(self) -> dict | list:
        return {
            "level": self.level.to_json(),
            "metadata": self.metadata.to_json(),
            "audio": self.audio.to_json() if self.audio is not None else None
        }

    @classmethod
    def _from_json_unwrap(cls, json_data: dict | list):
        return cls(
            level = Level.from_json(json_data["level"]),
            metadata = Metadata.from_json(json_data["metadata"]),
            audio = Audio.from_json(json_data["audio"]) if json_data["audio"] is not None else None,
        )


    @classmethod
    def combine_folders(cls, level_folders: list[LevelFolder], primary_level_folder: LevelFolder | None = None, combine_settings: l_versions.CombineSettings = l_versions.CombineSettings()):
        """Combines two level folders into one."""
        source = primary_level_folder if primary_level_folder is not None else level_folders[0]

        levels = [level_folder.level for level_folder in level_folders]
        level = source.version.combine_levels(levels, source.level, combine_settings)

        return cls(
            version = source.version,
            level = level,
            metadata = source.metadata,
            audio = source.audio
        )



class LevelFolderInfo(m_handlers.JSONFileHandler, m_handlers.FolderHandler):
    """Contains information about the level folder."""
    def __init__(
            self,
            level_folder: LevelFolder = LevelFolder(),
            themes: list[Theme] = None
        ):
        if themes is None:
            themes = []

        self.level_folder = level_folder
        self.themes = themes


    def to_json(self) -> dict | list:
        return {
            "level_folder": self.level_folder.to_json(),
            "themes": [theme.to_json() for theme in self.themes]
        }

    @classmethod
    def _from_json_unwrap(cls, json_data: dict | list):
        return cls(
            level_folder = LevelFolder.from_json(json_data["level_folder"]),
            themes = [Theme.from_json(theme_json) for theme_json in json_data["themes"]]
        )


    @classmethod
    def from_level_folder(cls, level_folder: LevelFolder, themes_folder_path: str):
        """Constructs from a level folder."""
        return cls(
            level_folder = level_folder,
            themes = level_folder.version.get_custom_themes_from_level(level_folder.level, themes_folder_path)
        )
