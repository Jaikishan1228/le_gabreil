import logging
from pathlib import Path
from typing import Optional, Iterator, Union
from logging import Logger, getLogger, StreamHandler

# setup default logger
defaultlogger = getLogger(__name__)
defaultlogger.setLevel(logging.INFO)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.INFO)
defaultlogger.addHandler(stream_handler)


class PythonTouch:
    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger or defaultlogger

    def touch(self, directory: Union[str, Path]):
        path = Path(directory)
        if path.exists() and not path.is_dir():
            self.logger.error(f"{directory} is not directory.")
            return

        if not (path.exists() or path.parent.exists()):
            self.logger.error(f"{directory} is not found.")
            return

        path.mkdir(exist_ok=True)

        for p in self._iter_recursively(path):
            self.logger.info(p)
            (p / "__init__.py").touch()

    def _iter_recursively(self, path: Path) -> Iterator[Path]:
        if not path.is_dir() or path.is_symlink():
            return
        yield path
        for p in path.iterdir():
            yield from self._iter_recursively(p)
