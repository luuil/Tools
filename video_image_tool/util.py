# coding: utf-8
# Created by luuil@outlook.com at 2021/5/27
import os
import logging
import enum
import json

LOGGING_FORMAT = '%(asctime)s|%(levelname)s|%(filename)s@%(funcName)s(%(lineno)d): %(message)s'


def set_default_logging(format: str = LOGGING_FORMAT, level=logging.DEBUG, **kwargs):
    logging.basicConfig(format=format, level=level, **kwargs)


class FileType(enum.Enum):
    File = 0,
    DIR = 1,
    LINK = 2,


def files_under(path: str, mode=0):
    path_join = os.path.join

    mode_type = FileType(mode)
    if mode_type == FileType.File:
        cond = os.path.isfile
    elif mode_type == FileType.DIR:
        cond = os.path.isdir
    elif mode_type == FileType.LINK:
        cond = os.path.islink
    else:
        logging.error(f'mode unsupported: {mode}')
        cond = lambda x: x

    names = os.listdir(path)
    files = [path_join(path, name) for name in names if cond(path_join(path, name))]
    return files


def json_load(path: str) -> dict:
    if not os.path.exists(path):
        return dict()
    with open(path, 'r') as f:
        return json.load(f)
