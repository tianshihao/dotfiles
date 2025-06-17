from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import Any

from .enums import ConfigurationType

JsonObject = dict[str, Any]  # Alias for the json loaded by the Loader


@dataclass
class Settings:
    """Represents the entire settings configuration."""
    applications: Applications

    @cached_property
    def all_configs_view(self) -> list[tuple[Configuration, Application]]:
        """Flattened view of all configurations with their corresponding application."""
        return [
            (configuration, application)
            for application in self.applications
            for configuration in application.configurations
        ]


@dataclass
class Application:
    """Represents an application with its configurations."""
    name: str
    configurations: Configurations


Applications = list[Application]


@dataclass
class Configuration:
    """Represents a configuration for an application."""
    type: ConfigurationType
    path_on_host: str
    path_in_repo: str
    excludes: list[str] = field(default_factory=list[str])


Configurations = list[Configuration]
