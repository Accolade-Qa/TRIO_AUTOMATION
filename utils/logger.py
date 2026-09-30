import logging
import os
from pathlib import Path

from config.global_var import (
    get_artifact_run_id,
    get_current_project,
    get_project_logs_path,
)


def _ensure_log_dir(log_file_path: Path):
    """Create logs directory if not present before the first log write."""
    log_dir = log_file_path.parent
    if not log_dir.is_dir():
        log_dir.mkdir(parents=True, exist_ok=True)


class _LazyFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=True):
        super().__init__(filename, mode=mode, encoding=encoding, delay=delay)
        self._dir_ensured = False

    def emit(self, record):
        if not self._dir_ensured:
            _ensure_log_dir(Path(self.baseFilename))
            self._dir_ensured = True
        return super().emit(record)


def enable_file_logging(project: str | None = None):
    """Activate lazy file logging for loggers created in this process."""
    global _FILE_LOGGING_ENABLED, _FILE_HANDLER

    if _FILE_LOGGING_ENABLED:
        return

    _FILE_LOGGING_ENABLED = True
    if _FILE_HANDLER is None:
        log_path = _get_log_file_path(project=project)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        _FILE_HANDLER = _LazyFileHandler(log_path, encoding="utf-8", delay=True)
        _FILE_HANDLER.setLevel(logging.DEBUG)
        _FILE_HANDLER.setFormatter(_FORMATTER)

    for logger in list(logging.root.manager.loggerDict.values()):
        if isinstance(logger, logging.Logger) and _FILE_HANDLER not in logger.handlers:
            logger.addHandler(_FILE_HANDLER)


def _suite_log_name(project: str | None = None) -> str:
    """Generate suite log file name."""
    project_name = project or get_current_project() or "lct"
    run_id = get_artifact_run_id()
    return f"{project_name}_{run_id}.log"


_LOG_FILE_PATH: Path | None = None
_LOG_FILE_PROJECT: str | None = None
_FILE_HANDLER: logging.FileHandler | None = None
_CONSOLE_HANDLER: logging.StreamHandler | None = None
_FILE_LOGGING_ENABLED = False
_FORMATTER = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")


def _get_log_file_path(project: str | None = None) -> Path:
    """Return single log file path for entire execution."""
    global _LOG_FILE_PATH, _LOG_FILE_PROJECT

    if _LOG_FILE_PATH is None or (_LOG_FILE_PROJECT is not None and project is not None and project != _LOG_FILE_PROJECT):
        _LOG_FILE_PROJECT = project
        _LOG_FILE_PATH = Path(get_project_logs_path(project=project)) / _suite_log_name(project=project)

    return _LOG_FILE_PATH


def get_logger(name: str) -> logging.Logger:
    """
    Return configured logger instance.
    Prevents duplicate handlers.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    global _FILE_HANDLER, _CONSOLE_HANDLER

    # File handler is delayed so imports/collection do not create empty log files.
    if _FILE_LOGGING_ENABLED:
        if _FILE_HANDLER is None:
            _FILE_HANDLER = _LazyFileHandler(
                _get_log_file_path(), encoding="utf-8", delay=True
            )
            _FILE_HANDLER.setLevel(logging.DEBUG)
            _FILE_HANDLER.setFormatter(_FORMATTER)
        if _FILE_HANDLER not in logger.handlers:
            logger.addHandler(_FILE_HANDLER)

    if _CONSOLE_HANDLER is None:
        _CONSOLE_HANDLER = logging.StreamHandler()
        _CONSOLE_HANDLER.setLevel(logging.INFO)
        _CONSOLE_HANDLER.setFormatter(_FORMATTER)

    logger.addHandler(_CONSOLE_HANDLER)

    return logger
