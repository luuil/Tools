# coding: utf-8
# author: luuil@outlook.com
# =============================================================
r'''Utils.'''

import os


def envs(*keys):
  """Get environment variables.

  Return:
    List of environment variable's value with the same length as
    parameter list.
  """
  _getenv = lambda key: os.getenv(key, default=None)
  vlist = list()
  for key in keys:
    vlist.append(_getenv(key))
  if len(vlist)==1:
    return vlist[0]
  return vlist