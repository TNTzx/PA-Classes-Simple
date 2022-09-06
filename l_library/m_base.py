"""Contains the base class."""


from __future__ import annotations


class PAMeta(type):
    """The base meta class."""
    def __repr__(cls):
        return cls.__name__


class PAObject(metaclass = PAMeta):
    """The base class for all PA classes."""
    def __repr__(self):
        variables = vars(self)

        inside_string = [
            f"{var_name} = {repr(var_value)}"
            for var_name, var_value in variables.items()
        ]

        inside_string = ", ".join(inside_string)

        return f"{type(self).__name__}({inside_string})"

    def __eq__(self, other: PAObject) -> bool:
        return repr(self) == repr(other)


class PAException(Exception):
    """The base PA exception class."""
