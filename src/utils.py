import os
import platform
from typing import Any, Callable

from .models import JsonObject


def get_platform_value(json_obj: JsonObject, key: str,  default_value: Any = None) -> Any:
    """Get a value from a dictionary based on the platform and key or return a default value."""
    platform_name: str = platform.system().lower()
    if not platform_name:
        raise ValueError("PLATFORM environment variable is not set.")
    if platform_name in json_obj and key in json_obj[platform_name]:
        return json_obj[platform_name][key]
    return json_obj.get(key, default_value)


def get_absolute_path(path: str) -> str:
    """Convert a path to an absolute path."""
    # todo tianshihao make sure the path is a path, it could be not exist, but it should bt a path.
    # Expand environment variables
    path = os.path.expandvars(path)
    # Expand '~' if present
    path = os.path.expanduser(path)
    # Normalize path separators
    path = os.path.normpath(path)
    # If already absolute, return as absolute
    if os.path.isabs(path):
        return os.path.abspath(path)
    # Otherwise, join with current working directory
    return os.path.abspath(os.path.join(os.getcwd(), path))


def make_ignore_function(excludes: list[str]) -> Callable[[str, list[str]], list[str]]:
    """Create a function to filter out excluded items from a list."""
    def ignore_func(directory: str, items: list[str]) -> list[str]:
        return [item for item in items if item in excludes]
    return ignore_func
