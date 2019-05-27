# coding: utf-8
# author: luuil@outlook.com
# created: 2018-11-29 15:01:10
# modified: 2019-04-04 11:45:09
# =============================================================
r"""Video segment tool"""

import cv2
import os
import logging
import time
import argparse
import numpy as np


def options():
  paser = argparse.ArgumentParser(description="""Cropping images with roi/percentage.
     for example: python imcrop.py -i "/data/in" -o "/data/out" -t 2 -r "0.5,0.5,0.5,0.5" """)
  paser.add_argument('-i', '--in_path', required=True, help='Image input path(parent directory)')
  paser.add_argument('-o', '--out_path', type=str, help='Image output path(parent directory)')
  paser.add_argument('-r', '--roi', required=True, type=str, help='roi that seprate by `,`')
  paser.add_argument('-t', '--roi_type', required=True, type=int, default=0, help='roi type:'
    """
    roitype          roi
         0(default) [x, y, w, h]      # actual roi
         1          [x1, y1, x2, y2]  # from up left (x1, y1) to bottom right (x2, y2)
         2          [xr, yr, wr, hr]  # roi ratio
    """)
  paser.add_argument('-s', '--subdir', type=int, default=0, help='if 1, travis subdir')
  args = paser.parse_args()
  return args

def roi2if(string, dtype):
  """string digits to integer or float."""
  l = string.split(",")
  if dtype == 2:
    l = [float(d) for d in l]
  else:
    l = [int(d) for d in l]
  return tuple(l)

def segloger(name, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
  logger = logging.getLogger(name)
  logger.setLevel(level)
  if not len(logger.handlers):
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(format))
    logger.addHandler(h)
  return logger


class ImCrop(object):
  """Image Crop"""
  def __init__(self, roi, roitype=0, lvl=logging.DEBUG):
    """
      roitype          roi
         0        [x, y, w, h]      # actual roi
         1        [x1, y1, x2, y2]  # from up left (x1, y1) to bottom right (x2, y2)
         2        [xr, yr, wr, hr]  # roi ratio
    """
    super(ImCrop, self).__init__()
    self._log = segloger("ImCrop")
    self._log.setLevel(lvl)

    self._roi = roi
    self._roitype = roitype

    self._log.info("roi: {}.".format(roi))
    
  @staticmethod
  def checkdir(dir):
    if not os.path.exists(dir):
      os.makedirs(dir)
      return False
    return True

  @staticmethod
  def read(impath, flag=cv2.IMREAD_COLOR):
    assert os.path.exists(impath), "can not open image: {}".format(impath)
    image = cv2.imread(impath, flag)
    return image

  def _actual_roi(self, w, h):
    def _between01(number):
      return number >=0. and number <= 1.

    roi = (0, 0, w, h)
    if self._roitype == 0:
      # to do: check valid
      roi = self._roi
    elif self._roitype == 1:
      # to do: check valid
      x1, y1, x2, y2 = self._roi
      roi = (x1, y1, x2 - x1, y2 - y1)
    elif self._roitype == 2:
      xr, yr, wr, hr = self._roi
      if _between01(xr) and _between01(yr) and _between01(wr) and _between01(hr) \
        and _between01(xr+wr) and _between01(yr+hr):
          nx = int(w * xr)
          ny = int(h * yr)
          nw = int(w * wr)
          nh = int(h * hr)
          nw = nw if nx + nw <= w else w - nx
          nh = nh if ny + nh <= h else h - ny
          self._log.debug('src:{}x{}; roi:[{},{},{},{}]([{},{},{},{}])'.format(
              w, h, nx, ny, nw, nh, xr, yr, wr, hr))
      roi = (nx, ny, nw, nh)
    return roi

  def crop(self, im):
    assert im is not None
    if im.ndim == 2:
        srch, srcw = im.shape
    if im.ndim == 3:
        srch, srcw, _ = im.shape
    x, y, w, h = self._actual_roi(srcw, srch)
    output = np.copy(im)
    return output[y:y+h, x:x+w]

  def multicrop(self, in_path, out_path, exts=["jpg", "png", "jpeg"]):
    assert os.path.exists(in_path)
    self.checkdir(out_path)
    imlist = [name for name in os.listdir(in_path) if name.split(".")[-1] in exts ]
    N = len(imlist)
    #for frame identity
    for n in range(0,N):
      impath = os.path.join(in_path, imlist[n])
      oimpath = os.path.join(out_path, imlist[n])
      im = self.read(impath)
      oim = self.crop(im)
      cv2.imwrite(oimpath, oim)
      self._log.info("({}/{}) {}".format(n, N, oimpath))

if __name__ == "__main__":
  options = options()
  # r"D:\hymlcv_svr\trunk\hycv_misc\classify\lolmatch\ingame_train_full"
  ic = ImCrop(roi2if(options.roi, options.roi_type), options.roi_type, logging.INFO)
  if options.subdir == 1:
    subdirs = [dirname for dirname in os.listdir(options.in_path)]
    for name in subdirs:
      in_path = os.path.join(options.in_path, name)
      out_path = os.path.join(options.out_path, name)
      ic.multicrop(in_path, out_path)
  else:
    out_path = options.out_path if options.out_path else "{}_corped".format(options.in_path)
    ic.multicrop(options.in_path, out_path)
