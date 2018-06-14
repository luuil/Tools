# coding: utf-8
# author: luuil@outlook.com

r"""Segment audio or video files to wav.

requirements:
  - http://www.ffmpeg.org/
  - pydub
"""

from audio_segment import MyAudioSegment
from audio_segment import semengt_by_label
from audio_segment import semengt_by_step
from audio_segment import total_length

### Tests ###

def test_MyAudioSegment():
  video_path = r'./test_data/sing_video.mp4'
  out_dir = r'./test_data/sing_mp4'
  mas = MyAudioSegment(video_path)
  # mas.export()
  n_step = mas.segment_second_step(out_dir, 3)
  n_file = mas.segment_with_label_file(r'./test_data/sing_video.txt', out_dir)
  print('segmented intervals count:', n_step)
  print('segmented files count:', n_file)


def test_semengt_by_step():
  in_dir = r'./test_data'
  out_dir = r'./test_data/semengt_by_step'
  time_step = 2
  offset = 1
  n_intervals, n_files = semengt_by_step(in_dir, out_dir, time_step, offset)
  print('segmented intervals: {}, files count: {}'.format(n_intervals, n_files))


def test_semengt_by_label():
  in_dir = r'./test_data'
  out_dir = r'./test_data/semengt_by_label'
  label_dir = r'./test_data'
  n_intervals, n_files = semengt_by_label(in_dir, out_dir, label_dir)
  print('segmented intervals: {}, files count: {}'.format(n_intervals, n_files))

def test_total_length():
  in_dir = r'./test_data'
  l = total_length(in_dir)
  print('Total length of all files in: [{}] '
    'is: {}s / {}min / {}h'.format(
    in_dir, l, l/60, l/3600))


if __name__ == '__main__':
  test_MyAudioSegment()
  test_semengt_by_step()
  test_semengt_by_label()
  test_total_length()
  pass