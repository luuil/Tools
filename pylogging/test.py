# coding: utf-8
# author: luuil@outlook.com
# created: 2019-10-23 17:57:20
# modified: 2019-10-23 18:44:15
# =============================================================
r"""Test logging."""

from core.logger import setup_logging
from core.logger import get_logger
from core.utils import envs


if __name__ == "__main__":
  import os

  # os.environ["LOG_CFG"] = "configs/logger_example.yaml"
  # os.environ["LOG_NAME"] = "example"

  os.makedirs("./logs", exist_ok=True)

  setup_logging()

  logger = get_logger("example")

  logger.debug("debug")
  logger.info("info")
  logger.warning("warn")
  logger.error("error")
