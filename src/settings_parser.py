import json
import logging
from typing import List

from .models import Application, Configuration
from .utils import get_absolute_path, get_platform_value


class SettingsParser:
    def __init__(self, settings_path: str = 'settings.json', platform: str = ''):
        self.settings_path = settings_path
        self.platform = platform
        self.settings = self._load_settings()
        if not self.platform:
            import platform as _platform
            self.platform = _platform.system()

    def _load_settings(self) -> dict:
        try:
            with open(self.settings_path, 'r') as file:
                data = json.load(file)
                if not isinstance(data, dict) or not data:
                    logging.error(
                        "settings.json is empty or not a valid dict.")
                    exit(1)
                return data
        except json.JSONDecodeError:
            logging.error("Error parsing settings.json", exc_info=True)
            exit(1)
        except FileNotFoundError:
            logging.error("settings.json not found", exc_info=True)
            exit(1)

    def parse(self) -> List[Application]:
        applications = []
        for application in self.settings['applications']:
            if get_platform_value(application, 'enable', self.platform):
                name = application['name']
                configurations = get_platform_value(
                    application, 'configurations', self.platform, default=[])
                parsed_configuration = []
                for configuration in configurations:
                    if get_platform_value(configuration, 'enable', self.platform, True):
                        type = configuration["type"]
                        path_on_host = get_absolute_path(get_platform_value(
                            configuration, 'path_on_host', self.platform))
                        path_in_repo = get_absolute_path(get_platform_value(
                            configuration, 'path_in_repo', self.platform))
                        excludes = get_platform_value(
                            configuration, 'excludes', self.platform)
                        parsed_configuration.append(Configuration(
                            type=type,
                            path_on_host=path_on_host,
                            path_in_repo=path_in_repo,
                            excludes=excludes
                        ))
                applications.append(Application(
                    name=name,
                    configurations=parsed_configuration
                ))
        logging.info(
            f"Loaded {len(applications)} applications, {sum(len(app.configurations) for app in applications)} configurations from settings.json.")
        return applications
