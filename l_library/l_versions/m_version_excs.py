"""Contains version-related exceptions."""


from .. import m_base


class VersionException(m_base.PAException):
    """The base version exception class."""


class VersionNotFound(VersionException):
    """The version can't be found."""
    def __init__(self, missing_version_number: str):
        super().__init__(f"Version with version number {missing_version_number} not found or is not supported.")
        self.missing_version_number = missing_version_number

class ImportException(VersionException):
    """There's an error in importing."""


class FolderNotFound(ImportException):
    """There's no folder."""
    def __init__(self, not_found_folder: str):
        super().__init__(f"Folder not found: {not_found_folder}")
        self.not_found_folder = not_found_folder


class LevelFileNotFound(ImportException):
    """The required level file is missing."""
    def __init__(self, level_folder_path: str, missing_file: str):
        super().__init__(f"Missing level file in {level_folder_path}: {missing_file}")
        self.level_folder_path = level_folder_path
        self.missing_file = missing_file

class IncompatibleVersionImport(ImportException):
    """The version is incompatible with the class you are using."""
    def __init__(self, level_folder_path: str, importing_version_num: str, current_version_num: str):
        super().__init__(f"The level folder {level_folder_path} with version {importing_version_num} is incompatible with version {current_version_num}.")
        self.level_folder_path = level_folder_path
        self.importing_version_num = importing_version_num
        self.current_version_num = current_version_num


class AudioNotPresent(ImportException):
    """The audio is not present."""
    def __init__(self):
        super().__init__("The audio is not present.")


class ThemeImportException(ImportException):
    """A theme import exception has occurred."""

class MissingThemes(ThemeImportException):
    """There are a few missing themes."""
    def __init__(self, missing_theme_ids: list[int]):
        super().__init__(f"Missing themes not found in themes folder. Missing theme IDs: {', '.join([str(theme_id) for theme_id in missing_theme_ids])}")
        self.missing_theme_ids = missing_theme_ids

class ThemeNotFound(ThemeImportException):
    """Theme not found in theme folder."""
    def __init__(self, missing_theme_id: int):
        super().__init__(f"Theme with ID {missing_theme_id} not found in themes folder.")
        self.missing_theme_id = missing_theme_id

class NoThemesInFolder(ThemeImportException):
    """There's no themes in the theme folder."""
    def __init__(self):
        super().__init__("There are no detectable themes in the themes folder. Make sure there are valid themes in the folder.")
