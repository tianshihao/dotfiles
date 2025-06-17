from .enums import ConfigurationType
from .models import Application, Configuration, JsonObject, Settings
from .utils import get_absolute_path, get_platform_value


class Parser:
    """Parse raw settings JSON into structured Settings dataclass."""

    def __init__(self) -> None:
        pass

    def parse(self, raw_settings: JsonObject) -> Settings:
        """Parse raw settings dict to Settings dataclass."""
        return self._parse_settings(raw_settings)

    def _parse_settings(self, raw_settings: JsonObject) -> Settings:
        """Parse the top-level settings dict."""
        return Settings(
            applications=[
                self._parse_application(application)
                for application in raw_settings['applications']
                if get_platform_value(application, 'enable', default_value=False)
            ]
        )

    def _parse_application(self, application: JsonObject) -> Application:
        """Parse a single application dict."""
        return Application(
            name=application['name'],
            configurations=[
                self._parse_configuration(configuration)
                for configuration in get_platform_value(application, 'configurations', default_value=[])
                if get_platform_value(configuration, 'enable', default_value=True)
            ]
        )

    def _parse_configuration(self, configuration: JsonObject) -> Configuration:
        """Parse a single configuration dict."""
        return Configuration(
            type=ConfigurationType(configuration["type"]),
            path_on_host=get_absolute_path(get_platform_value(
                configuration, 'path_on_host', default_value='')),
            path_in_repo=get_absolute_path(get_platform_value(
                configuration, 'path_in_repo', default_value='')),
            excludes=get_platform_value(
                configuration, 'excludes', default_value=[])
        )
