from typing import List, Optional, Dict, Any
import argparse
import json
import os
import platform
import shutil
import sys
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-7s %(filename)s:%(lineno)d %(message)s'
)


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


class Manager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):  # Prevents re-initialization
            self.settings: Dict[str, Any] = self._load_settings()
            self.platform: str = platform.system()
            self.applications: List[Application] = []

            self._parse_settings()

            self.initialized = True  # Mark as initialized

    def retrieve_from_host(self) -> None:
        self._filter()
        self._copy('path_on_host', 'path_in_repo', 'Retrieving')

    def dispatch_to_host(self) -> None:
        self._copy('path_in_repo', 'path_on_host', 'Dispatching')

    def _copy(self, src_attr: str, dst_attr: str, action_desc: str) -> None:
        total_applications = len(self.applications)
        total_configurations = sum(len(app.configurations)
                                   for app in self.applications)
        logging.info(
            f"{action_desc}: {total_applications} applications, {total_configurations} configurations to process.")

        copied_config_count = 0
        app_index = 0
        for application in self.applications:
            app_index += 1
            for idx, configuration in enumerate(application.configurations, 1):
                copied_config_count += 1
                src = getattr(configuration, src_attr)
                dst = getattr(configuration, dst_attr)
                excludes = list(configuration.excludes or [])
                logging.info(
                    f"[{copied_config_count}/{total_configurations}] {action_desc} {configuration.type} '{src}' <-> '{dst}' for application '{application.name}'"
                )
                if configuration.type == 'directory':
                    shutil.copytree(
                        src, dst,
                        ignore=self._make_ignore_function(excludes),
                        dirs_exist_ok=True
                    )
                elif configuration.type == 'file':
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                else:
                    logging.error(
                        f"Unknown configuration type '{configuration.type}' for '{src}'")
        logging.info(
            f"{action_desc} finished: {total_applications} applications, {copied_config_count} configurations processed.")

    def _load_settings(self) -> dict:
        try:
            with open('settings.json', 'r') as file:
                data = json.load(file)
                if not isinstance(data, dict) or not data:
                    logging.error(
                        "settings.json is empty or not a valid dict.")
                    exit(1)
                return data
        except json.JSONDecodeError as e:
            logging.error(
                "Error parsing settings.json", exc_info=True)
            exit(1)
        except FileNotFoundError as e:
            logging.error(
                "settings.json not found", exc_info=True)
            exit(1)

    def _parse_settings(self) -> None:
        for application in self.settings['applications']:
            if self._get_platform_value(application, 'enable', self.platform):
                name = application['name']
                configurations = self._get_platform_value(
                    application, 'configurations', self.platform, default=[])

                parsed_configuration = []
                for configuration in configurations:
                    if self._get_platform_value(configuration, 'enable', self.platform, True):
                        type = configuration["type"]
                        path_on_host = self._get_absolute_path(self._get_platform_value(
                            configuration, 'path_on_host', self.platform))
                        path_in_repo = self._get_absolute_path(self._get_platform_value(
                            configuration, 'path_in_repo', self.platform))
                        excludes = self._get_platform_value(
                            configuration, 'excludes', self.platform)

                        parsed_configuration.append(Configuration(
                            type=type,
                            path_on_host=path_on_host,
                            path_in_repo=path_in_repo,
                            excludes=excludes
                        ))

                self.applications.append(Application(
                    name=name,
                    configurations=parsed_configuration
                ))

        logging.info(
            f"Loaded {len(self.applications)} applications, {sum(len(app.configurations) for app in self.applications)} configurations from settings."
        )

    def _filter(self) -> None:
        total_configs = sum(len(app.configurations)
                            for app in self.applications)
        skipped_configs = 0
        for application in self.applications:
            to_remove = []
            for configuration in application.configurations:
                if not os.path.isdir(configuration.path_on_host) and not os.path.isfile(configuration.path_on_host):
                    logging.warning(
                        f"Application '{application.name}' has a configuration path '{configuration.path_on_host}' that does not exist on the host, skipping.")
                    to_remove.append(configuration)
                    skipped_configs += 1
                    continue

            for invalid in to_remove:
                application.configurations.remove(invalid)
        to_remove = None

        self.applications = [
            app for app in self.applications if app.configurations]

        remaining_configs = sum(len(app.configurations)
                                for app in self.applications)
        if self.applications:
            logging.info(
                f"Processed configurations for {len(self.applications)} applications. "
                f"Remaining: {remaining_configs} configurations, Skipped: {skipped_configs} of {total_configs}."
            )
        else:
            logging.warning(
                "No valid applications found after processing configurations, exiting.")
            sys.exit(0)

    def _get_platform_value(self, obj: dict, key: str, platform: str, default=None) -> Any:
        platform = platform.lower()
        if platform in obj and key in obj[platform]:
            return obj[platform][key]
        return obj.get(key, default)

    def _get_absolute_path(self, path: str) -> str:
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

    def _make_ignore_function(self, excludes: List[str]):
        def ignore_func(directory, items):
            return [item for item in items if item in excludes]
        return ignore_func


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Manage configuration synchronization.')
    parser.add_argument('--retrieve', action='store_true',
                        help='Retrieve configurations from the host')
    parser.add_argument('--dispatch', action='store_true',
                        help='Dispatch configurations to the host')

    args = parser.parse_args()

    manager = Manager()

    if args.dispatch:
        manager.dispatch_to_host()
    elif args.retrieve:
        manager.retrieve_from_host()
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
