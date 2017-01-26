import logging
from logging import NullHandler

from .api import WordPress  # NOQA F401

__all__ = ['WordPress']

logging.getLogger(__name__).addHandler(NullHandler())
