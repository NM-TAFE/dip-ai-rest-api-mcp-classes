"""Shared logging configuration helpers for MCP servers."""
from __future__ import annotations

import logging.config
from pathlib import Path
from typing import Dict, Iterable, Mapping, Sequence

def build_log_config(
    log_file: Path | str,
    *,
    logger_handlers: Mapping[str, Sequence[str]] | None = None,
    console: bool = True,
    root_level: str = "INFO",
    logger_level: str = "DEBUG",
) -> Dict:
    """Construct a dictConfig for rotating file logging.

    Parameters
    ----------
    log_file: Path | str
        Destination log file; parent directories are created automatically.
    logger_handlers: Mapping[str, Sequence[str]] | None
        Optional mapping of logger name -> handler names. If omitted, no named
        loggers are configured beyond the root logger.
    console: bool
        Whether to also log to stdout via ``logging.StreamHandler``.
    root_level: str
        Logging level for the root logger.
    logger_level: str
        Logging level applied to any named loggers provided.
    """

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Base handlers
    handlers = {
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": str(log_path),
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 3,
            "encoding": "utf-8",
            "delay": True,
        },
    }

    if console:
        handlers["console"] = {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }

    # Default formatter and an access-style formatter for HTTP logs
    formatters = {
        "default": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "access": {
            "format": '%(asctime)s [%(levelname)s] %(client_addr)s - "%(request_line)s" %(status_code)s'
        },
    }

    loggers: Dict[str, Dict] = {}
    if logger_handlers:
        for name, handler_list in logger_handlers.items():
            loggers[name] = {
                "level": logger_level,
                "handlers": list(handler_list),
                "propagate": False,
            }

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters,
        "handlers": handlers,
        "loggers": loggers,
        "root": {"level": root_level, "handlers": [h for h in handlers.keys()]},
    }

    return config


def configure_logging(config: Mapping) -> None:
    """Apply a ``dictConfig`` built by ``build_log_config``."""

    logging.config.dictConfig(config)

__all__ = ["build_log_config", "configure_logging"]
