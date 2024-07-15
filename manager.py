from typing import List, Optional, Dict, Any
import argparse
import json
import os
import platform
import shutil


class SyncSetting:
    def __init__(self, name: str, enable: bool, source: str, target: str, excludes: List[str]) -> None:
        self.name: str = name
        self.enable: bool = enable
        self.source: str = source
        self.target: str = target
        self.excludes: List[str] = excludes


class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):  # Prevents re-initialization
            self.settings: Optional[Dict[str, Any]] = self.__load_settings()
            self.platform: str = platform.system()
            self.configs: List[SyncSetting] = []
            self.__parse_config()
            self.initialized = True  # Mark as initialized

    def get_platform(self) -> str:
        return self.platform

    def dispatch_to_host(self) -> None:
        for config in self.configs:
            if config.enable:
                # Determine the target directory
                target_dir = os.path.dirname(config.target)

                # Remove the existing target, whether it's a file or directory
                if os.path.exists(config.target):
                    if os.path.isdir(config.target):
                        shutil.rmtree(config.target)
                    else:
                        os.remove(config.target)

                # Ensure the target directory exists
                os.makedirs(target_dir, exist_ok=True)
                ignore_func = make_ignore_function(config.excludes)
                if os.path.isdir(config.source):
                    shutil.copytree(
                        config.source, config.target, ignore=ignore_func)
                else:
                    shutil.copy(config.source, config.target)

    def retrieve_from_host(self) -> None:
        for config in self.configs:
            if config.enable:
                # Ensure the source directory exists (where we're copying back to)
                source_dir = os.path.dirname(config.source)
                os.makedirs(source_dir, exist_ok=True)
                ignore_func = make_ignore_function(config.excludes)

                # Check if the target exists and is a directory or a file
                if os.path.exists(config.target):
                    # If it's a directory, use shutil.copytree, else use shutil.copy
                    if os.path.isdir(config.target):
                        # If the source directory already exists, remove it first
                        if os.path.exists(config.source):
                            shutil.rmtree(config.source)
                        shutil.copytree(
                            config.target, config.source, ignore=ignore_func)
                    else:
                        # If it's a file, simply copy it back
                        shutil.copy(config.target, config.source)
                else:
                    print(
                        f"Warning: Target {config.target} does not exist. Skipping.")

    def sync(self) -> None:
        print("todo: sync")

    def merge(self) -> None:
        print("todo: merge")

    def __load_settings(self) -> None:
        try:
            with open('settings.json', 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
        except FileNotFoundError as e:
            print(f"Configuration file not found: {e}")

    def __parse_config(self) -> None:
        if self.settings is not None:
            for config in self.settings['configurations']:
                # Default configuration
                name = config['name']
                enable = config['enable']
                source = config['source']
                target = config['target']
                excludes = config.get('excludes', [])

                # Platform specific overrides
                platform_config = config.get(
                    'platform', {}).get(self.platform, {})
                enable = platform_config.get('enable', enable)
                source = platform_config.get('source', source)
                target = platform_config.get('target', target)
                excludes = platform_config.get('excludes', excludes)

                if enable:
                    source_path = os.path.join(os.getcwd(), source)
                    target_path = os.path.join(
                        os.path.expanduser(target), source)
                    self.configs.append(SyncSetting(
                        name, enable, source_path, target_path, excludes))


def make_ignore_function(excludes):
    def _ignore_function(directory, contents):
        return [content for content in contents if content in excludes]
    return _ignore_function


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Manage configuration synchronization.')
    parser.add_argument('--dispatch', action='store_true',
                        help='Dispatch configurations to the host')
    parser.add_argument('--retrieve', action='store_true',
                        help='Retrieve configurations from the host')
    parser.add_argument('--merge', action='store_true',
                        help='Merge configurations between host and repository')

    args = parser.parse_args()

    config_manager = ConfigManager()

    if args.dispatch:
        config_manager.dispatch_to_host()
    elif args.retrieve:
        config_manager.retrieve_from_host()
    elif args.merge:
        config_manager.merge()
    else:
        print("No valid operation specified. Use --help for more information.")


if __name__ == '__main__':
    main()
