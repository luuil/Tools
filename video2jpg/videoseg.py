# coding: utf-8
# author: luuil@outlook.com
# created: 2018-11-29 15:01:10
# modified: 2019-04-04 11:44:51
# =============================================================
r"""Video segment tool"""

import cv2
import os
import logging
import time
import argparse


def options():
  paser = argparse.ArgumentParser(description='Extracting frames from video with step(default=1).')
  paser.add_argument('-i', '--in_path', required=True, help='Video path(or parent directory if `mode==1`)')
  paser.add_argument('-o', '--out_path', type=str, help='Image save path(parent directory)')
  paser.add_argument('-s', '--step', type=int, default=1, help='Step(greater or equal to 1, default=1)')
  paser.add_argument('-m', '--mode', type=int, default=0, help='`in_path` is actual video path if equal to 0(default), '
    'else parent directory')
  args = paser.parse_args()
  return args


def segloger(name, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
  logger = logging.getLogger(name)
  logger.setLevel(level)
  if not len(logger.handlers):
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(format))
    logger.addHandler(h)
  return logger


class VideoSeg(object):
  """docstring for VideoSeg"""
  def __init__(self, step=1):
    super(VideoSeg, self).__init__()
    self._log = segloger("VideoSeg")

    assert step >= 1, "step must greater or equal to 1."
    self._step = step
    
  @staticmethod
  def checkdir(dir):
    if not os.path.exists(dir):
      os.makedirs(dir)

  def seg(self, video_path, out_path):
    self.checkdir(out_path)

    # set video file path of input video with name and extension
    self._vid = cv2.VideoCapture(video_path)

    self._log.info("Processing...{}".format(video_path))

    #for frame identity
    index = 0
    while(True):
        # Extract images
        ret, frame = self._vid.read()
        
        # end of video
        if not ret: break
        
        # next frame
        index += 1
        
        # step over
        if index != 1 and index % self._step != 0:   
          continue

        # Saves images
        out_name = os.path.join(out_path, "frame.{}.{}.jpg".format(int(time.time()), index))
        self._log.info("Extracting...{}".format(out_name))
        cv2.imwrite(out_name, frame)

        if self._step > 1:
          self._log.info("Skiping...frame{}~frame{}".format(index, index + self._step))

    self._vid.release()


def list_videos(path, exts=["mp4", "mkv"]):
  video_list = [name for name in os.listdir(in_path) if name.split(".")[-1] in exts]
  return video_list


if __name__ == "__main__":
  options = options()
  vs = VideoSeg(options.step)

  if options.mode == 0:
    # if not specified, mkdir with the same name as video itself
    out_path = options.out_path if options.out_path else \
      os.path.splitext(options.in_path)[0]
    vs.seg(options.in_path, out_path)
  else:
    video_dir = options.in_path #r"F:\videos\lolmatch"
    video_list = sorted(list_videos(video_dir))
    for name in video_list:
      out_path = os.path.join(video_dir, name[:-4]) if not options.out_path \
        else os.path.join(options.out_path, name[:-4])
      if VideoSeg.checkdir(out_path): continue
      video_path = os.path.join(video_dir, name)
      vs.seg(video_path, out_path)