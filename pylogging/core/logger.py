# coding: utf-8
# author: luuil@outlook.com
# =============================================================
r'''Logging.'''

import yaml
import logging.config
import sys
import os

from .utils import envs


def setup_logging(
  default_config="configs/logger_example.yaml",
  default_level=logging.INFO,
  ):
  """Set Logging up."""
  path = default_config
  if os.path.exists(path):
    with open(path, 'rt', encoding="utf-8") as f:
      config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
  else:
    logging.basicConfig(level=default_level)


def get_logger(name="example"):
  """Get logger for a given name."""
  return logging.getLogger(name)
