import logging
import os
import shutil
from typing import Any, Callable

from .enums import ActionDesc, ConfigurationType
from .loader import Loader
from .models import Configuration, JsonObject, Settings
from .parser import Parser
from .utils import make_ignore_function
from .validator import Validator


class Worker:
    """Handle configuration synchronization tasks."""

    def __init__(self, settings_path: str, app_filter: list[str] | None = None) -> None:
        _loader: Loader = Loader()
        _validator: Validator = Validator()
        _parser: Parser = Parser()

        _json_obj: JsonObject = _loader.load(settings_path)
        _validator.validate(_json_obj)
        self._settings: Settings = _parser.parse(_json_obj)
        self._app_filter: list[str] | None = app_filter

        self._action_map: dict[
            ActionDesc,
            tuple[
                Callable[..., Any],
                tuple[
                    Callable[[Configuration], str],
                    Callable[[Configuration], str],
                    Callable[[Configuration], list[str]]
                ]
            ]
        ] = {
            ActionDesc.RETRIEVE: (
                self._operation_copy,
                (lambda c: c.path_on_host, lambda c: c.path_in_repo,
                 lambda c: list(c.excludes or []))
            ),
            ActionDesc.DISPATCH: (
                self._operation_copy,
                (lambda c: c.path_in_repo, lambda c: c.path_on_host,
                 lambda c: list(c.excludes or []))
            ),
            ActionDesc.OVERVIEW: (
                self._operation_overview,
                (lambda c: c.path_in_repo, lambda c: c.path_on_host,
                 lambda c: [])
            ),
        }

    def run(self, action_desc: ActionDesc) -> None:
        """Run the specified action on the configurations."""
        if action_desc not in self._action_map:
            logging.error(f"Unknown action: {action_desc}")
            return

        operation_func, (src_getter, dst_getter,
                         excludes_getter) = self._action_map[action_desc]

        all_configs_view = self._settings.all_configs_view
        if self._app_filter:
            all_configs_view = [
                (cfg, app) for (cfg, app) in all_configs_view if app.name in self._app_filter
            ]
        total_configs = len(all_configs_view)
        logging.info(
            f"{action_desc.value}: {total_configs} configurations to process.")

        for idx, (configuration, application) in enumerate(all_configs_view, 1):
            src = src_getter(configuration)
            dst = dst_getter(configuration)
            excludes = excludes_getter(configuration)
            operation_func(configuration, src, dst, excludes)
            logging.info(
                f"[Cfg {idx}/{total_configs}] {action_desc.value} {application.name} {configuration.type} '{src}' ==> '{dst}'"
            )

        logging.info(
            f"{action_desc.value} finished: {total_configs} configurations processed.")

    def _operation_copy(self, configuration: Configuration, src: str, dst: str, excludes: list[str]) -> None:
        try:
            match configuration.type:
                case ConfigurationType.DIRECTORY:
                    shutil.copytree(
                        src, dst,
                        ignore=make_ignore_function(excludes),
                        dirs_exist_ok=True
                    )
                case ConfigurationType.FILE:
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                case ConfigurationType.SYMLINK:
                    # todo tianshihao
                    pass
        except Exception as e:
            logging.error(
                f"Failed to copy {configuration.type.value} '{src}' ==> '{dst}' for application '{getattr(configuration, 'name', 'unknown')}'. Reason: {e}"
            )

    def _operation_overview(self, configuration: Configuration, src: str, dst: str, excludes: list[str]) -> None:
        pass
