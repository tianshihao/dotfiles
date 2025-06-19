from typing import Any, Set, cast

from .models import JsonObject


class Validator:
    """Validate the settings loaded from the configuration file."""

    PLATFORM_KEYS: Set[str] = {"windows", "linux", "darwin"}
    APPLICATION_KEYS: Set[str] = {
        "name", "enable", "configurations", *PLATFORM_KEYS}
    CONFIGURATION_KEYS: Set[str] = {
        "type", "enable", "path_on_host", "path_in_repo", "excludes", *PLATFORM_KEYS}

    def __init__(self) -> None:
        self._errors: list[str] = []

    def validate(self, json_obj: JsonObject) -> None:
        self._errors.clear()
        self._validate_root(json_obj)
        if self._errors:
            error_report: str = "Validator found the following errors in settings.json:\n" + \
                "\n".join(self._errors)
            raise ValueError(error_report)

    def _type_name(self, value: Any) -> str:
        return type(value).__name__

    def _validate_root(self, data: JsonObject) -> None:
        applications: Any = data.get("applications")
        if applications is None:
            self._errors.append("'applications' field is missing.")
            return
        if not isinstance(applications, list):
            self._errors.append(
                f"'applications' should be list, got {self._type_name(applications)}: {applications}")
            return
        applications_cast: list[JsonObject] = cast(
            list[JsonObject], applications)
        for idx, application in enumerate(applications_cast):
            self._validate_application(application, idx)

    def _validate_application(self, application: Any, idx: int) -> None:
        if not isinstance(application, dict):
            self._errors.append(
                f"applications[{idx}] should be object, got {self._type_name(application)}: {application}")
            return
        app_cast: dict[str, Any] = cast(dict[str, Any], application)
        # Only allowed keys
        for key in app_cast:
            if key not in self.APPLICATION_KEYS:
                self._errors.append(
                    f"applications[{idx}] has invalid key '{key}'.")
        # name
        name = app_cast.get("name")
        if not isinstance(name, str):
            self._errors.append(
                f"applications[{idx}].name should be str, got {self._type_name(name)}: {name}")
        # enable
        enable = app_cast.get("enable")
        if not isinstance(enable, bool):
            self._errors.append(
                f"applications[{idx}].enable should be bool, got {self._type_name(enable)}: {enable}")
        # configurations
        configurations = app_cast.get("configurations")
        if not isinstance(configurations, list):
            self._errors.append(
                f"applications[{idx}].configurations should be list, got {self._type_name(configurations)}: {configurations}")
        else:
            configs_cast: list[Any] = cast(list[Any], configurations)
            for j, config in enumerate(configs_cast):
                self._validate_configuration(config, idx, j)
        # platform-specific fields
        for plat in self.PLATFORM_KEYS:
            if plat in app_cast:
                self._validate_platform_config(
                    app_cast[plat], idx, plat, context="application")

    def _validate_configuration(self, config: Any, app_idx: int, cfg_idx: int) -> None:
        if not isinstance(config, dict):
            self._errors.append(
                f"applications[{app_idx}].configurations[{cfg_idx}] should be object, got {self._type_name(config)}: {config}")
            return
        cfg_cast: dict[str, Any] = cast(dict[str, Any], config)
        # type
        type_val = cfg_cast.get("type")
        if not (isinstance(type_val, str) and type_val in {"file", "directory", "link"}):
            self._errors.append(
                f"applications[{app_idx}].configurations[{cfg_idx}].type should be 'file', 'directory', or 'link', got {self._type_name(type_val)}: {type_val}")
        # path_on_host
        poh = cfg_cast.get("path_on_host")
        if not isinstance(poh, str):
            self._errors.append(
                f"applications[{app_idx}].configurations[{cfg_idx}].path_on_host should be str, got {self._type_name(poh)}: {poh}")
        # path_in_repo
        pir = cfg_cast.get("path_in_repo")
        if not isinstance(pir, str):
            self._errors.append(
                f"applications[{app_idx}].configurations[{cfg_idx}].path_in_repo should be str, got {self._type_name(pir)}: {pir}")
        # excludes
        excludes = cfg_cast.get("excludes")
        if excludes is not None:
            if not isinstance(excludes, list):
                self._errors.append(
                    f"applications[{app_idx}].configurations[{cfg_idx}].excludes should be list, got {self._type_name(excludes)}: {excludes}")
            else:
                excludes_cast: list[Any] = cast(list[Any], excludes)
                for k, item in enumerate(excludes_cast):
                    if not isinstance(item, str):
                        self._errors.append(
                            f"applications[{app_idx}].configurations[{cfg_idx}].excludes[{k}] should be str, got {self._type_name(item)}: {item}")
        # platform-specific fields
        for plat in self.PLATFORM_KEYS:
            if plat in cfg_cast:
                self._validate_platform_config(
                    cfg_cast[plat], app_idx, f"configurations[{cfg_idx}].{plat}", context="configuration")

    def _validate_platform_config(self, plat_obj: Any, idx: int, plat: str, context: str) -> None:
        if not isinstance(plat_obj, dict):
            self._errors.append(
                f"applications[{idx}].{plat} should be object, got {self._type_name(plat_obj)}: {plat_obj}")
            return
        plat_obj_cast: dict[str, Any] = cast(dict[str, Any], plat_obj)
        if context == "application":
            allowed_keys = self.APPLICATION_KEYS
        elif context == "configuration":
            allowed_keys = self.CONFIGURATION_KEYS
        else:
            allowed_keys: Set[str] = set()
        for key in plat_obj_cast:
            if key not in allowed_keys:
                self._errors.append(
                    f"applications[{idx}].{plat} has invalid key '{key}'.")
