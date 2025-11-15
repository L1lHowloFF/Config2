import json
import os
from typing import Dict, Any


class Config:
    def __init__(self, config_data: Dict[str, Any]):
        self.package_name = config_data.get("package_name", "")
        self.repository_url = config_data.get("repository_url", "")
        self.test_mode = config_data.get("test_mode", False)
        self.test_repository_path = config_data.get("test_repository_path", "")
        self.output_filename = config_data.get("output_filename", "dependencies_graph.png")
        self.ascii_tree_output = config_data.get("ascii_tree_output", False)

    @classmethod
    def load_from_file(cls, file_path: str) -> 'Config':

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            return cls(config_data)
        except FileNotFoundError:
            raise ConfigError(f"Config file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise ConfigError(f"Error loading config: {e}")

    def validate(self) -> None:
        errors = []

        if not self.package_name or not self.package_name.strip():
            errors.append("Package name cannot be empty")

        if not self.test_mode and (not self.repository_url or not self.repository_url.strip()):
            errors.append("Repository URL cannot be empty in non-test mode")

        if self.test_mode and (not self.test_repository_path or not self.test_repository_path.strip()):
            errors.append("Test repository path cannot be empty in test mode")

        if not self.output_filename or not self.output_filename.strip():
            errors.append("Output filename cannot be empty")

        if errors:
            raise ConfigError("Configuration validation errors:\n" + "\n".join(f"  - {error}" for error in errors))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "package_name": self.package_name,
            "repository_url": self.repository_url,
            "test_mode": self.test_mode,
            "test_repository_path": self.test_repository_path,
            "output_filename": self.output_filename,
            "ascii_tree_output": self.ascii_tree_output
        }


class ConfigError(Exception):
    pass