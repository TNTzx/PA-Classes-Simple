"""Contains exceptions about levels."""


from . import m_base


class LevelException(m_base.PAException):
    """Represents an exception from levels."""


class AudioImportException(LevelException):
    """The audio isn't imported correctly."""
    def __init__(self, incorrect_path: str):
        self.incorrect_path = incorrect_path
        super().__init__(f"Cannot find audio for path: {incorrect_path}.")


class FromJSONException(LevelException):
    """An exception occurred while decoding the JSON and transforming it to an object."""
    def __init__(self, error_message: str):
        super().__init__(f"Exception raised when decoding to JSON: {error_message}")
