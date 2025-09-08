import os
from pathlib import Path
from typing import Iterator, List, Optional
import logging
from ..config.settings import settings

logger = logging.getLogger(__name__)

class FileScanner:
    def __init__(self):
       self.max_file_size = settings.get_max_file_size()
       self.allowed_extensions = settings.get_file_extensions()
       self.follow_symlinks = settings.should_follow_symlinks()

    def scan_files(self) -> Iterator[Path]:
        search_dirs = settings.get_search_directories()

        if not search_dirs:
            logger.warning("No search directories found in config")
            return

        for dir_path in search_dirs:
            logger.info(f"Scanning directory: {dir_path}")
            yield from self._scan_directory(dir_path)

    def _scan_directory(self, directory: Path) -> Iterator[Path]:
        try:
            for item in directory.rglob('*'):
                if self._should_include_file(item):
                    yield item
        except PermissionError:
            logger.warning(f"Permission denied: {directory}")
        except Exception as e:
            logger.error(f"Error scanning directory: {directory}: {e}")

    def _should_include_file(self, file_path: Path) -> bool:
        if not file_path.is_file():
            return False
        if file_path.is_symlink() and not self.follow_symlinks:
            return False
        if self.allowed_extensions and file_path.suffix.lower() not in self.allowed_extensions:
            return False
        try:
            if file_path.stat().st_size > self.max_file_size:
                return False
        except Exception as e:
            logger.warning(f"Error getting file size: {file_path}: {e}")
            return False

        return True

    def count_files(self) -> int:
        return sum(1 for _ in self.scan_files())

        