import logging
import os
import shutil
import sys
from typing import List

from .settings_parser import SettingsParser
from .utils import make_ignore_function


class Worker:
    def __init__(self, platform: str):
        self.parser = SettingsParser(platform=platform)
        self.applications = self.parser.parse()
        self.manager = None  # Optional, can be set later if needed

    def run(self, src_attr: str, dst_attr: str, action_desc) -> None:
        total_applications = len(self.applications)
        total_configurations = sum(len(app.configurations)
                                   for app in self.applications)
        logging.info(
            f"{action_desc.value}: {total_applications} applications, {total_configurations} configurations to process.")
        processed_configurations_count = 0
        for app_idx, application in enumerate(self.applications, 1):
            for cfg_idx, configuration in enumerate(application.configurations, 1):
                processed_configurations_count += 1
                src = getattr(configuration, src_attr)
                dst = getattr(configuration, dst_attr)
                excludes = list(configuration.excludes or [])
                if action_desc.value == 'Retrieving' or action_desc.value == 'Dispatching':
                    self._operation_copy(configuration, src, dst, excludes)
                else:
                    self._operation_validate(configuration, src, dst)
                logging.info(
                    f"[App {app_idx}/{total_applications} | Cfg {cfg_idx}/{len(application.configurations)} | Total {processed_configurations_count}/{total_configurations}] "
                    f"{action_desc.value} {configuration.type} '{src}' <-> '{dst}' for application '{application.name}'"
                )
        logging.info(
            f"{action_desc.value} finished: {total_applications} applications, {processed_configurations_count} configurations processed.")

    def filter(self) -> None:
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

    def _operation_copy(self, configuration, src: str, dst: str, excludes: List[str]) -> None:
        if configuration.type == 'directory':
            shutil.copytree(
                src, dst,
                ignore=make_ignore_function(excludes),
                dirs_exist_ok=True
            )
        elif configuration.type == 'file':
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        else:
            logging.error(
                f"Unknown configuration type '{configuration.type}' for '{src}'")

    def _operation_validate(self, configuration, src: str, dst: str) -> None:
        pass
