import os
import yaml
from pathlib import Path
from typing import Dict, List, Any

class Settings:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._get_default_config_path()
        self config = self._load_config()

    def _get_default_config_path(self) -> Path:
        current_dir = Path(__file__).parent.parent.parent
        return current_dir / "config.yaml"

    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config file: {e}")

    def get_search_directories(self) -> List[str]:
        directories = self.config.get('search_directories', [])
        for dir_path in directories:
            expanded_path = os.path.expanduser(dir_path)
            if expanded_path.exists() and expanded_path.is_dir():
                directories.append(expanded_path)
        return directories

    def get_file_extensions(self, category: str = None) -> List[str]:
        file_types = self.config.get('file_types', {})
        if category:
            return file_types.get(category, [])
        all_extensions = []
        for extensions in file_types.values():
            all_extensions.extend(extensions)
        return all_extensions

    def get_max_file_size(self) -> int:
        max_size_mb = self.config.get('search', {}).get('max_file_size_mb', 50)
        return max_size_mb * 1024 * 1024

   def should_index_content(self) -> bool:
        return self.config.get('search', {}).get('index_content', True)

    def should_follow_symlinks(self) -> bool:
        return self.config.get('search', {}).get('follow_symlinks', True)

    def get_auto_refresh_hours(self) -> int:
        return self.config.get('indexing', {}).get('auto_refresh_hours', 24)

    def get_batch_size(self) -> int:
        return self.config.get('indexing', {}).get('batch_size', 100)

settings = Settings()