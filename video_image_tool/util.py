# coding: utf-8
# Created by luuil@outlook.com at 2021/5/27
import logging

LOGGING_FORMAT = '%(asctime)s|%(levelname)s|%(filename)s@%(funcName)s(%(lineno)d): %(message)s'


def set_default_logging(format: str = LOGGING_FORMAT, level=logging.DEBUG, **kwargs):
    logging.basicConfig(format=format, level=level, **kwargs)
