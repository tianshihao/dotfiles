import os
from typing import Any, List


def get_platform_value(obj: dict, key: str, platform: str, default=None) -> Any:
    platform = platform.lower()
    if platform in obj and key in obj[platform]:
        return obj[platform][key]
    return obj.get(key, default)


def get_absolute_path(path: str) -> str:
    # Expand '~' if present
    if path.startswith('~'):
        path = os.path.expanduser(path)
    # Normalize path separators
    norm_path = os.path.normpath(path)
    # If already absolute, return as absolute
    if os.path.isabs(norm_path):
        return os.path.abspath(norm_path)
    # Otherwise, join with current working directory
    return os.path.abspath(os.path.join(os.getcwd(), norm_path))


def make_ignore_function(excludes: List[str]):
    def ignore_func(directory, items):
        return [item for item in items if item in excludes]
    return ignore_func
