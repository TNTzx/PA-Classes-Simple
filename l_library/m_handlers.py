"""Contains the main manager class."""


import json

from . import m_disk_utils, m_base, m_level_excs


class Handler(m_base.PAObject):
    """Parent class for all handlers."""


class JSONClassHandler(Handler):
    """A JSON handler for classes."""
    @classmethod
    def to_json(cls):
        """Turns this class to a JSON."""


    @classmethod
    def _from_json_unwrap(cls, json_data: dict | list):
        """Returns a class from JSON. This is the function called to transform the JSON to this object."""
        return cls

    @classmethod
    def from_json(cls, json_data: dict | list):
        """Returns a class from JSON. Raises FromJSONException if there's an error."""
        try:
            return cls._from_json_unwrap(json_data)
        except (KeyError, IndexError) as exc:
            raise m_level_excs.FromJSONException(str(exc))


class JSONHandler(Handler):
    """Parent class for handling input and output."""
    def to_json(self) -> dict | list:
        """Turns this object to a JSON."""
        return {}


    @classmethod
    def _from_json_unwrap(cls, json_data: dict | list):
        """Creates an object from JSON. This is the function called to transform the JSON to this object."""
        return cls()

    @classmethod
    def from_json(cls, json_data: dict | list):
        """Creates an object from JSON. Raises FromJSONException if there's an error."""
        try:
            return cls._from_json_unwrap(json_data)
        except (KeyError, IndexError) as exc:
            raise m_level_excs.FromJSONException(str(exc))


class FileHandler(Handler):
    """Parent class for handling files."""
    file_ext: str = "pcm"

    @classmethod
    def append_file_ext(cls, filename: str):
        """Appends the file extension to the file name."""
        return f"{filename}.{cls.file_ext}"

    def to_file(self, folder_path: str, filename: str):
        """Outputs this object to a file."""

    @classmethod
    def from_file(cls, file_path: str):
        """Creates this object to a file."""


class RawFileHandler(Handler):
    """Parent class for handling raw files such as `.lsb`."""
    raw_file_ext: str

    @classmethod
    def append_file_ext_raw(cls, filename: str):
        """Appends the file extension to the file name."""
        return f"{filename}.{cls.raw_file_ext}"

    def to_file_raw(self, folder_path: str, filename: str):
        """Outputs this object to a raw file."""

    @classmethod
    def from_file_raw(cls, file_path: str):
        """Creates this object to a raw file."""


class FolderHandler(Handler):
    """A handler for writing to a folder."""
    def to_folder(self, folder_path: str):
        """Creates the folder."""

    @classmethod
    def from_folder(self, folder_path: str):
        """Creates this object from the folder path."""


class JSONFileHandler(JSONHandler, FileHandler):
    """Contains both a JSON and file handler."""
    def to_file(self, folder_path: str, filename: str):
        json_data = self.to_json()
        m_disk_utils.override_file(
            folder_path,
            self.append_file_ext(filename),
            json.dumps(
                json_data,
                indent = "\t",
                ensure_ascii = False
            )
        )

    @classmethod
    def from_file(cls, file_path: str):
        json_data = m_disk_utils.read_file(file_path)
        json_data = json.loads(json_data)
        return cls.from_json(json_data)
