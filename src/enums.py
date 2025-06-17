from enum import Enum


class ActionDesc(Enum):
    """Synchronization action descriptor."""
    VALIDATE = 'Validating'
    OVERVIEW = 'Overviewing'
    RETRIEVE = 'Retrieving'
    DISPATCH = 'Dispatching'

    def __str__(self) -> str:
        return self.value


class ConfigurationType(Enum):
    """Types of configurations."""
    FILE = 'file'
    DIRECTORY = 'directory'
    SYMLINK = 'symlink'

    def __str__(self) -> str:
        return self.value
