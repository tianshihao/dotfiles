import json

from .models import JsonObject


class Loader:
    """Load settings from a JSON file."""

    def __init__(self) -> None:
        pass

    def load(self, settings_path: str) -> JsonObject:
        """Load settings from the JSON file, returning a Setting object."""
        with open(settings_path, 'r', encoding='utf-8') as file:
            json_obj: JsonObject = json.load(file)
            if not json_obj:
                raise ValueError(
                    f"{settings_path} is empty or not a valid dict.")
            return json_obj
