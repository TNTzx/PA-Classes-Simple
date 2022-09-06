"""Contains the 20.4.4 parser."""


from __future__ import annotations

import typing as typ

import os
import json
import copy

from ... import m_disk_utils, m_level_data, m_level_excs
from .. import m_branches, m_combine_settings, m_version_excs, m_versions



class v20_4_4(m_versions.PAVersion):
    """The 20.4.4 version."""
    version_number: str = "20.4.4"
    branch = m_branches.Legacy


    @classmethod
    def get_version_number(cls, level: m_level_data.Level):
        try:
            return level.data["level_data"]["level_version"]
        except KeyError:
            return None

    @classmethod
    def is_compatible_level(cls, level: m_level_data.Level):
        return cls.get_version_number(level) == cls.version_number


    @classmethod
    def import_level_folder(cls, level_folder: str, themes_folder: str, load_audio: bool = True) -> m_level_data.LevelFolder:
        def get_path_from_folder(filename: str):
            """Gets the path of the filename from the level folder."""
            return os.path.join(level_folder, filename)

        def get_data_in_level_folder(filename: str):
            """Returns the contents of the file inside of the level folder."""
            path = get_path_from_folder(filename)
            file = m_disk_utils.read_file(path)
            return json.loads(file)

        if not m_disk_utils.path_exists(level_folder):
            raise m_version_excs.FolderNotFound(level_folder)


        try:
            metadata = m_level_data.Metadata(get_data_in_level_folder("metadata.lsb"))
            level = m_level_data.Level(get_data_in_level_folder("level.lsb"))

            if load_audio:
                try:
                    audio = m_level_data.Audio.from_path(get_path_from_folder("level.ogg"))
                except m_level_excs.AudioImportException as exc:
                    raise m_version_excs.LevelFileNotFound(
                        os.path.split(exc.incorrect_path)[1]
                    ) from exc
            else:
                audio = None

        except FileNotFoundError as exc:
            raise m_version_excs.LevelFileNotFound(
                os.path.split(exc.filename)[1]
            ) from exc


        if not cls.is_compatible_level(level):
            level_version_num = cls.get_version_number(level)
            if level_version_num is None:
                level_version_num = "cannot detect"
            raise m_version_excs.IncompatibleVersion(level_version_num, cls.version_number)

        themes = cls.get_custom_themes_from_level(level, themes_folder)


        return m_level_data.LevelFolder(version = cls, level = level, audio = audio, metadata = metadata, themes = themes)


    @classmethod
    def get_custom_themes_from_level(cls, level: m_level_data.Level, themes_folder: str) -> list[m_level_data.Theme]:
        level_theme_ids = cls.get_theme_ids_from_level(level)
        themes = cls.get_all_themes_in_folder(themes_folder)

        level_themes: list[m_level_data.Theme] = []
        level_theme_ids_buffer = copy.deepcopy(level_theme_ids)

        for theme in themes:
            theme_id = int(theme.data["id"])
            if theme_id in level_theme_ids:
                level_themes.append(theme)
                level_theme_ids_buffer.remove(theme_id)

        if len(level_theme_ids_buffer) > 0:
            raise m_version_excs.MissingThemes(level_theme_ids_buffer)

        return level_themes


    @classmethod
    def get_theme_ids_from_level(cls, level: m_level_data.Level):
        theme_keyframes: list[dict[typ.Literal["x", "ct"], str]] = level.data["events"]["theme"]

        theme_ids: list[int] = []

        for theme_keyframe in theme_keyframes:
            theme_id = int(theme_keyframe["x"])
            if theme_id > 8:
                theme_ids.append(theme_id)

        return theme_ids


    @classmethod
    def get_theme_from_id(cls, themes_folder: str, theme_id: int) -> m_level_data.Theme:
        themes = cls.get_all_themes_in_folder(themes_folder)
        for theme in themes:
            if int(theme.data["id"]) == theme_id:
                return theme

        raise m_version_excs.ThemeNotFound(theme_id)


    @classmethod
    def get_all_themes_in_folder(cls, themes_folder: str) -> list[m_level_data.Theme]:
        if not m_disk_utils.path_exists(themes_folder):
            raise m_version_excs.FolderNotFound(themes_folder)

        theme_paths = m_disk_utils.get_all_file_paths_in_folder(themes_folder)
        theme_paths = [
            theme_path
            for theme_path in theme_paths
            if os.path.splitext(theme_path)[1] == ".lst"
        ]

        themes: list[m_level_data.Theme] = []
        for theme_path in theme_paths:
            try:
                theme_data: dict[str, str] = json.loads(
                    m_disk_utils.read_file(theme_path)
                )
                int(theme_data["id"])
                themes.append(m_level_data.Theme(theme_data))
            except (KeyError, json.JSONDecodeError):
                continue

        if len(themes) == 0:
            raise m_version_excs.NoThemesInFolder()

        return themes


    default_checkpoint: dict = {"active": "False", "name": "Base Checkpoint", "t": "0", "pos": {"x": "0", "y": "0"}}
    default_event_kfs: dict[str, list] = {
        "pos": [{"t":"0","x":"0","y":"0"}],
        "zoom": [{"t":"0","x":"20"}],
        "rot": [{"t":"0","x":"0"}],
        "shake": [{"t":"0","x":"0","y":"0"}],
        "theme": [{"t":"0","x":"0"}],
        "chroma": [{"t":"0","x":"0"}],
        "bloom": [{"t":"0","x":"0"}],
        "vignette": [{"t":"0","x":"0","y":"0","z":"0","x2":"0","y2":"0","z2":"0"}],
        "lens": [{"t":"0","x":"0"}],
        "grain": [{"t":"0","x":"0","y":"0","z":"0"}]
    }

    @classmethod
    def combine_levels(cls, levels: list[m_level_data.Level], primary_level: m_level_data.Level = None, combine_settings: m_combine_settings.CombineSettings = m_combine_settings.CombineSettings()):
        # Initialize level elements
        combined_beatmap_objects: list[dict] = []

        combined_imported_prefabs: list[dict] = []
        combined_prefab_objects: list[dict] = []

        combined_markers: list[dict] = []

        combined_checkpoints: list[dict] = []

        event_kf_names = list(cls.default_event_kfs)
        combined_event_keyframes: dict[str, list] = {kf_name: [] for kf_name in event_kf_names}

        combined_bg_objects: list[dict] = []


        # Make copies of stuff to not modify objects
        copied_levels = [copy.deepcopy(level) for level in levels]

        # Get primary and source levels
        if primary_level is not None:
            copied_primary_level = copy.deepcopy(primary_level)
            source_level = copy.deepcopy(copied_primary_level)
        else:
            copied_primary_level = None
            source_level = copy.deepcopy(copied_levels[0])


        def delete_first_alg(level_element_list: list, delete_first: bool):
            """Deletes the first object from the list if `delete_first` is True. Returns the list after."""
            if delete_first:
                return level_element_list[1:]

            return level_element_list

        # Combine!
        for level in copied_levels:
            if combine_settings.include_beatmap_objects:
                combined_beatmap_objects += level.data["beatmap_objects"]

            if combine_settings.include_prefabs:
                combined_imported_prefabs += level.data["prefabs"]
                combined_prefab_objects += level.data["prefab_objects"]

            if combine_settings.include_markers:
                combined_markers += level.data["ed"]["markers"]

            if combine_settings.include_checkpoints:
                combined_checkpoints += delete_first_alg(
                    level.data["checkpoints"],
                    combine_settings.delete_first_checkpoint
                )

            if combine_settings.include_event_keyframes:
                for kf_name in event_kf_names:
                    combined_event_keyframes[kf_name] += delete_first_alg(
                        level.data["events"][kf_name],
                        combine_settings.delete_first_event_keyframes
                    )

            if combine_settings.include_bg_objects:
                combined_bg_objects += level.data["bg_objects"]


        # Make sure that the initial stuff required for the level are there!
        if not combine_settings.include_checkpoints:
            combined_checkpoints = [cls.default_checkpoint]
        if not combine_settings.include_event_keyframes:
            combined_event_keyframes = cls.default_event_kfs



        def insert_first_object_if_deleted(level_element: list, is_deleted: bool, to_insert: list[dict]):
            """Reinserts the first object of the source level to the level element list if it was deleted earlier."""
            if is_deleted:
                level_element.insert(0, to_insert[0])


        # Copy source level then add the combined level elements
        combined_level_data = copy.deepcopy(source_level.data)


        combined_level_data["beatmap_objects"] = combined_beatmap_objects

        combined_level_data["prefabs"] = combined_imported_prefabs
        combined_level_data["prefab_objects"] = combined_prefab_objects

        combined_level_data["ed"]["markers"] = combined_markers

        combined_level_data["checkpoints"] = combined_checkpoints
        insert_first_object_if_deleted(
            combined_level_data["checkpoints"],
            combine_settings.delete_first_checkpoint,
            source_level.data["checkpoints"]
        )

        combined_level_data["events"] = combined_event_keyframes
        if combine_settings.delete_first_event_keyframes:
            for kf_name in event_kf_names:
                insert_first_object_if_deleted(
                    combined_level_data["events"][kf_name],
                    True,
                    source_level.data["events"][kf_name]
                )

        combined_level_data["bg_objects"] = combined_bg_objects


        combined_level = m_level_data.Level(combined_level_data)

        if copied_primary_level is not None:
            combined_level: m_level_data.Level = cls.combine_levels([copied_primary_level, combined_level])

        return combined_level
