"""Contains classes for branches."""


from .. import m_base


class Branch(m_base.PAObject):
    """Represents a version branch."""
    name: str


class Legacy(Branch):
    """The legacy branch."""
    name: str = "legacy"
