"""Logging for the ``koor`` command-line layer.

The thesis scripts keep their ``print`` statements (their console output is part
of the recorded experiment logs); this module only configures the ``koor``
logger used by :mod:`koor.cli` to record *what* was run, with which arguments
and configuration, and how long it took. A console handler always writes to
stderr; an optional file handler appends the same records to ``logfile``.
"""
import logging
import os
import sys

LOGGER_NAME = "koor"
FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level="INFO", logfile=None, stream=None):
    """Configure and return the ``koor`` logger.

    ``level`` is a logging level name or number; ``logfile`` (optional) is a
    path that receives the same records (UTF-8, append mode; parent directory
    is created). Calling this more than once replaces the previous handlers
    instead of stacking them, so it is safe in tests and in ``python -m``
    re-entry. The logger does not propagate to the root logger, so scripts
    that configure ``logging`` themselves are unaffected.
    """
    if isinstance(level, str):
        lvl = logging.getLevelName(level.upper())
        if not isinstance(lvl, int):
            raise ValueError(f"unknown log level: {level!r}")
        level = lvl
    logger = logging.getLogger(LOGGER_NAME)
    for h in list(logger.handlers):
        logger.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass
    logger.setLevel(level)
    logger.propagate = False
    fmt = logging.Formatter(FORMAT, DATEFMT)

    console = logging.StreamHandler(stream or sys.stderr)
    console.setFormatter(fmt)
    logger.addHandler(console)

    if logfile:
        logfile = os.path.abspath(os.path.expanduser(str(logfile)))
        d = os.path.dirname(logfile)
        if d:
            os.makedirs(d, exist_ok=True)
        fh = logging.FileHandler(logfile, mode="a", encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


def get_logger():
    """The ``koor`` logger (a NullHandler is attached if nothing configured it)."""
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())
    return logger
