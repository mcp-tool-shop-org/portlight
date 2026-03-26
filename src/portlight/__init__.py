"""Portlight — trade-first maritime strategy game."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

try:
    __version__ = _pkg_version("portlight")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
