# coding: utf-8
# author: luuil@outlook.com

r"""Segment audio or video files to wav.

requirements:
  - http://www.ffmpeg.org/
  - pydub
"""

from __future__ import print_function
import os.path
from pydub import AudioSegment
import util

SUPPORTED_FORMAT = ['mkv', 'mp4', 'flv', 'wav']
AUDIO_FORMAT = 'wav'

class MyAudioSegment(object):
  """Wapper for AudioSegment."""
  def __init__(self, video, verbose=False):
    super(MyAudioSegment, self).__init__()
    assert util.is_exists(video)
    self.__audio = AudioSegment.from_file(video)

    self.length_in_seconds = int(self.__audio.duration_seconds)
    self.length_in_miliseconds = len(self.__audio)
    
    file_dir, file_name, file_ext = util.file_path_info(video)
    self.name = file_name
    self.__dir = file_dir
    self.__ext = file_ext

    if verbose:
      self.summary()


  def summary(self):
    info = '\nFile info:\n'\
           'length(ms){tabs}'\
           'length(s){tabs}'\
           'extension{tabs}'\
           'name{tabs}'\
           'location{tabs}\n'\
           '{len_ms}ms{tabs}'\
           '{len_s}s{tabs}'\
           '{ext}{tabs}'\
           '{name}{tabs}'\
           '{dir}\n'\
           .format(
            len_s=self.length_in_seconds,
            len_ms=self.length_in_miliseconds,
            name=self.name,
            dir=self.__dir,
            ext=self.__ext,
            tabs=''.join(['\t']*2)
            )
    print(info)


  def __slice(self, start, end):
    """Audio slice."""
    assert start <= self.length_in_miliseconds, 'Start points exceed '\
      'the length of audio'
    exceed_end = end > self.length_in_miliseconds
    return self.__audio[start:end], exceed_end


  def __export_slice(self, out_dir, start, end):
    """Export audio slice."""
    audio_slice, exceed_end = self.__slice(start, end)
    if exceed_end:
      print('Warning: end point exceed audio length, skipping..')
      return
    util.maybe_create_directory(out_dir)
  
    out_name ='{basename}_{start}_{end}.wav'.format(basename=self.name,
      start=int(start/1000), end=int(end/1000))
    out_path =  os.path.join(out_dir, out_name)
    print('Segment time interval(in seconds) '\
      '[{start} ~ {end}]: {out_path}'.format(out_path=out_path,
                                             start=int(start/1000),
                                             end=int(end/1000)))
    if not util.is_exists(out_path, verbose=False):
      audio_slice.export(out_path, format=AUDIO_FORMAT)


  def export(self):
    """Export whole audio file"""
    self.__export_slice(self.__dir, 0, self.length_in_miliseconds)


  def segment_second_interval(self, out_dir, start, end, offset=0):
    """Segment by time interval(in seconds)."""
    # Move forward and cut out the same length
    assert offset <= (end - start), 'offset should be short than time step.'
    if offset > 0 and (start + offset < end):
      interval = end - start
      n = 0
      for new_start in range(start, end, offset):
        if new_start >= self.length_in_seconds: break
        new_end = new_start + interval
        if new_end >= self.length_in_seconds: break
        self.__export_slice(out_dir, new_start*1000, new_end*1000)
        n += 1
      return n
    else:
        self.__export_slice(out_dir, start*1000, end*1000)
        return 1


  def segment_second_step(self, out_dir, time_step, offset=0):
    """Segment by time step."""
    assert time_step >=0, 'time step should >= 0.'
    n = 0
    for start in range(0, self.length_in_seconds, time_step):
      end = start + time_step
      n += self.segment_second_interval(out_dir, start, end, offset)
    return n


  def segment_with_label_file(self, label_file, out_dir, offset=0):
    """Segment by label file.

    contents in label file as below:
      ```
      2,5\n
      6,10\n
      120,150
      ```
    i.e., one line for one interval(in seconds)
    """
    with open(label_file, mode='r') as ofile:
      n = 0
      for line in ofile:
        points = line.strip().split(',')
        start, end = int(points[0]), int(points[1])
        self.segment_second_interval(out_dir, start, end, offset)
        n += 1
    return n


### Warppers ###

def semengt_by_step(in_dir, out_dir, time_step, offset=0):
  """Segment by time steps(in seconds)."""
  filenames = []
  for ext in SUPPORTED_FORMAT:
    filenames.extend(util.get_filenames(in_dir, extention=ext))
  print(filenames)
  N = 0
  for fname in filenames:
    fpath = os.path.join(in_dir, fname)
    mas = MyAudioSegment(fpath, verbose=True)
    n = mas.segment_second_step(out_dir, time_step, offset)
    N += n
  return N, len(filenames)


def semengt_by_label(in_dir, out_dir, label_dir, offset=0):
  """Segment audio by time interval(in seconds)."""
  filenames = []
  for ext in SUPPORTED_FORMAT:
    filenames.extend(util.get_filenames(in_dir, extention=ext))
  print(filenames)
  N = 0
  for fname in filenames:
    fpath = os.path.join(in_dir, fname)
    mas = MyAudioSegment(fpath)
    label_filename = mas.name + '.txt'
    label_path = os.path.join(label_dir, label_filename)
    if not util.is_exists(label_path): continue
    n = mas.segment_with_label_file(label_path, out_dir, offset)
    N += n
  return N, len(filenames)


def total_length(in_dir):
  """Calculate the total length of all files(in seconds)."""
  filenames = []
  for ext in SUPPORTED_FORMAT:
    filenames.extend(util.get_filenames(in_dir, extention=ext))
  print(filenames)
  length = 0
  for fname in filenames:
    fpath = os.path.join(in_dir, fname)
    mas = MyAudioSegment(fpath)
    length += mas.length_in_seconds
    print('Length of {} is {}s'.format(fpath, length))
  return length


### Tests ###

def test_MyAudioSegment():
  video_path = r'../video/20180521/1ce1183155f6a8e153bb8ed92f101e1d.mp4'
  out_dir = r'./test_MyAudioSegment'
  mas = MyAudioSegment(video_path)
  # mas.export()
  n_step = mas.segment_second_step(out_dir, 5)
  n_file = mas.segment_with_label_file(r'./test_label.txt', out_dir)
  print('segmented intervals count:', n_step)
  print('segmented intervals count:', n_file)


def test_semengt_by_step():
  in_dir = r'../wav/20180521/other'
  out_dir = r'../wav/20180521/5s_3offest/zother'
  time_step = 5
  offset = 3
  n_intervals, n_files = semengt_by_step(in_dir, out_dir, time_step, offset)
  print('segmented intervals: {}, files count: {}'.format(n_intervals, n_files))


def test_semengt_by_label():
  in_dir = r'../video/20180521'
  out_dir = r'./out_by_label'
  label_dir = r'../annotation/20180521'
  n_intervals, n_files = semengt_by_label(in_dir, out_dir, label_dir)
  print('segmented intervals: {}, files count: {}'.format(n_intervals, n_files))

def test_total_length():
  in_dir = r'../video/20180521'
  l = total_length(in_dir)
  print('Total length of all files in: [{}] '
    'is: {}s / {}min / {}h'.format(
    in_dir, l, l/60, l/3600))


if __name__ == '__main__':
  # test_MyAudioSegment()
  # test_semengt_by_step()
  # test_semengt_by_label()
  # test_total_length()
  pass