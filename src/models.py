from enum import Enum
from typing import List, Optional


class ActionDesc(Enum):
    RETRIEVE = 'Retrieving'
    DISPATCH = 'Dispatching'
    VALIDATE = 'Validating'


class Application:
    def __init__(self, name: str, configurations: List['Configuration']) -> None:
        self.name: str = name
        self.configurations: List['Configuration'] = configurations


class Configuration:
    def __init__(self, type: str, path_on_host: str, path_in_repo: str, excludes: Optional[List[str]] = None) -> None:
        self.type: str = type
        self.path_on_host: str = path_on_host
        self.path_in_repo: str = path_in_repo
        self.excludes: List[str] = excludes if excludes is not None else []
