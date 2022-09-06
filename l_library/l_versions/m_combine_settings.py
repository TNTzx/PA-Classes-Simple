"""Contains combine settings."""


from .. import m_base


class CombineSettings(m_base.PAObject):
    """Represents settings for combining."""
    def __init__(
            self,
            include_beatmap_objects: bool = True,
            include_prefabs: bool = True,
            include_markers: bool = True,
            include_checkpoints: bool = True,
            include_event_keyframes: bool = True,
            include_bg_objects: bool = True,

            delete_first_checkpoint: bool = True,
            delete_first_event_keyframes: bool = True
        ):
        self.include_beatmap_objects = include_beatmap_objects
        self.include_prefabs = include_prefabs
        self.include_markers = include_markers
        self.include_checkpoints = include_checkpoints
        self.include_event_keyframes = include_event_keyframes
        self.include_bg_objects = include_bg_objects

        self.delete_first_checkpoint = delete_first_checkpoint
        self.delete_first_event_keyframes = delete_first_event_keyframes
