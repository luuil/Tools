import os

def is_exists(path, verbose=True):
  exists = os.path.exists(path)
  if not exists and verbose:
    print('Warning: {} not exists.'.format(path))
  return exists


def check_ext(path, extention):
  """是否为指定后缀."""
  return os.path.splitext(path)[1] == '.' + extention


def get_filenames(path, extention='mp4'):
  """获取文件名列表."""
  names = [filename for filename in os.listdir(path)
           if check_ext(filename, extention)]
  return names

def file_path_info(path):
  """获取目录名, 文件名和后缀名."""
  filename = os.path.basename(path)
  dirname = os.path.dirname(path)
  filename, ext = os.path.splitext(filename)
  return dirname, filename, ext

def maybe_create_directory(path):
  """检查文件夹是否存在, 不存在则创建."""
  if not is_exists(path):
    print('Create directory: {}'.format(path))
    os.makedirs(path)


def maybe_create_file(filename):
  """检查文件是否存在, 不存在则创建空文件."""
  if not is_exists(filename):
    print('create: {}'.format(filename))
    with open(filename, 'w'):
        pass
  else:
    print('exists: {}'.format(filename))


def generate_empty_annotation_files(video_path, annotation_path):
  """生成空标注文件"""
  mp4s = util.get_filenames(video_path, extention='mp4')
  anns = [mp4[:-3]+'txt' for mp4 in mp4s]
  ann_paths = [os.path.join(annotation_path, name) for name in anns]
  for ann in ann_paths:
      util.maybe_create_file(ann)
  print('count: {}'.format(len(ann_paths)))


if __name__ == '__main__':
  # version = 20180521
  # video_path = '../test_data'.format(version=version)
  # annotation_path = '../annotation/{version}'.format(version=version)
  # generate_empty_annotation_files(video_path, annotation_path)
  # print(file_path_info('./path/s/xx.wav'))
  pass