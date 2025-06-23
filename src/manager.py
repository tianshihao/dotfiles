from __future__ import annotations

from .enums import ActionDesc
from .worker import Worker


class Manager:
    """Singleton manager for configuration synchronization."""
    _instance: Manager | None = None

    def __new__(cls, settings_path: str, app_filter: list[str] | None = None) -> Manager:
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
        return cls._instance

    def __init__(self, settings_path: str, app_filter: list[str] | None = None) -> None:
        if not hasattr(self, 'initialized'):
            self._settings_path: str = settings_path
            self._app_filter: list[str] | None = app_filter
            self._worker: Worker = Worker(self._settings_path, app_filter=self._app_filter)
            self._initialized: bool = True

    def validate(self) -> None:
        """Validate the settings and configurations."""
        self._worker.run(ActionDesc.VALIDATE)

    def overview(self) -> None:
        """Output the configurations that will be synchronized (dry run)."""
        self._worker.run(ActionDesc.OVERVIEW)

    def retrieve_from_host(self) -> None:
        """Retrieve configurations from the host."""
        self._worker.run(ActionDesc.RETRIEVE)

    def dispatch_to_host(self) -> None:
        """Dispatch configurations to the host."""
        self._worker.run(ActionDesc.DISPATCH)
