"""Contains exceptions about levels."""


class LevelException(Exception):
    """Represents an exception from levels."""


class AudioImportException(LevelException):
    """The audio isn't imported correctly."""
    def __init__(self, incorrect_path: str):
        self.incorrect_path = incorrect_path
        super().__init__(f"Cannot find audio for path: {incorrect_path}.")
