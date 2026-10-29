# -*- coding: utf-8 -*-
"""
Configuration manager.
"""
import json
import os
import sys
from typing import Any, Dict

from .base_manager import BaseManager


if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")


class ConfigManager(BaseManager):
    def __init__(self, config_file_path: str = ""):
        BaseManager.__init__(self)

        self._config: Dict[str, Any] = {}
        self._config_file_path: str = ""

        if config_file_path:
            self._config_file_path = config_file_path
            self.load_config(self._config_file_path)

    @staticmethod
    def _get_user_config_dir() -> str:
        base_dir = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
        return os.path.join(base_dir, "EORS")

    @staticmethod
    def _get_bundled_config_path() -> str:
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, "P02_Resource", "configs", "config.json")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "..", "..", "P02_Resource", "configs", "config.json")

    def _sanitize_paths(self):
        folders = self._config.get("foldersPath", {})
        if not isinstance(folders, dict):
            return

        for key in ("datasetPath", "imagePath"):
            value = folders.get(key)
            if value and not os.path.exists(value):
                folders[key] = ""

        default_path = folders.get("defaultPath")
        if not default_path or not os.path.exists(default_path):
            folders["defaultPath"] = os.path.expanduser("~")

    def _load_default_config(self) -> bool:
        bundled_config_path = self._get_bundled_config_path()
        if not os.path.exists(bundled_config_path):
            return False

        current_config_path = self._config_file_path
        if not self.load_config(bundled_config_path):
            return False

        self._config_file_path = current_config_path
        self._sanitize_paths()
        return True

    def load_config(self, config_file_path: str = "") -> bool:
        try:
            if config_file_path:
                self._config_file_path = config_file_path

            if not os.path.exists(self._config_file_path):
                print(f"配置文件不存在: {self._config_file_path}")
                return False

            with open(self._config_file_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)

            print(f"成功加载配置文件: {self._config_file_path}")
            return True
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            return False

    def save_config(self, config_file_path: str = "") -> bool:
        try:
            save_path = config_file_path if config_file_path else self._config_file_path
            save_dir = os.path.dirname(save_path)
            if save_dir:
                os.makedirs(save_dir, exist_ok=True)

            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, ensure_ascii=False, indent=4)

            print(f"成功保存配置文件: {save_path}")
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False

    def get(self, key_path: str, default: Any = None) -> Any:
        try:
            keys = key_path.split(".") if isinstance(key_path, str) else key_path
            value = self._config

            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default

            return value
        except Exception:
            return default

    def set(self, key_path: str, value: Any) -> bool:
        try:
            keys = key_path.split(".") if isinstance(key_path, str) else key_path
            current = self._config

            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]

            current[keys[-1]] = value
            self.save_config()
            return True
        except Exception as e:
            print(f"设置配置项失败: {str(e)}")
            return False

    def initialize(self):
        if self._is_initialized:
            return True

        super().initialize()

        if not self._config_file_path:
            if hasattr(sys, "_MEIPASS"):
                self._config_file_path = os.path.join(self._get_user_config_dir(), "config.json")
            else:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                self._config_file_path = os.path.join(
                    current_dir, "..", "..", "P02_Resource", "configs", "config.json"
                )

        if not self.load_config():
            if self._load_default_config():
                self.save_config()
            else:
                self.save_config()
        else:
            self._sanitize_paths()
            if hasattr(sys, "_MEIPASS"):
                self.save_config()

        print(f"ConfigManager初始化完成，配置文件路径: {self._config_file_path}")
        return True

    def shutdown(self):
        self.save_config()
        self._is_initialized = False
        print("ConfigManager已关闭")
        return True
