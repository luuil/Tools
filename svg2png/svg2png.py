# coding: utf-8
# author: luuil@outlook.com
# =============================================================
r"""Convert SVG to PNG via svgexport.

svgexport: https://github.com/shakiba/svgexport
"""

import os
import logging
import argparse as Args

# set target default size to 32:?
CONVERT_ONE = "svgexport {svg} {png} 32:"


def set_logger(name):
  logger = logging.getLogger(name)
  handler = logging.StreamHandler()
  handler.setFormatter(
    logging.Formatter("%(asctime)s %(name)s %(levelname)s %(filename)s %(lineno)d %(message)s"))
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)
  logger.propogate = False
  return logger


class SVG2PNG(object):
  """Convert SVG to PNG."""
  def __init__(self):
    super(SVG2PNG, self).__init__()
    self._log = set_logger("SVG2PNG")

  def _check(self, file):
    _, suffix = os.path.splitext(file)
    if suffix != ".svg":
      self._log.warn("Not SVG file: {}, skiping".format(file))
      return False
    return True

  def convert(self, svg, png=None):
    if not self._check(svg):
      return
    prefix, sufix = os.path.splitext(svg)
    if png is None:
      png = "{}.png".format(prefix)
    if os.path.exists(png):
      self._log.info("Exists already: {}, skiping".format(png))
      return
    cmd = CONVERT_ONE.format(svg=svg, png=png)
    self._log.info(cmd)
    os.system(cmd)

  def convert_directory(self, input_dir, output_dir=None):
    files = os.listdir(input_dir)
    n, N = 1, len(files)
    for f in files:
      self._log.info("progress: {}/{}".format(n, N))
      n += 1
      fname, _ = os.path.splitext(f)
      if output_dir is None:
        out_png = os.path.join(input_dir, "{}.png".format(fname))
      else:
        if not os.path.exists(output_dir):
          os.makedirs(output_dir)
        out_png = os.path.join(output_dir, "{}.png".format(fname))
      in_svg  = os.path.join(input_dir, f)
      self.convert(in_svg, out_png)



def parse_args():
  paser = Args.ArgumentParser(description='Convert SVG to PNG via `svgexport`.')
  paser.add_argument('input', help="input SVG file or directory which contains SVG files")
  paser.add_argument('-o', '--output', help="output PNG file or directory where to store PNG files")
  paser.add_argument('-d', '--directory_mode', action='store_true', help="directory mode")
  
  args    = paser.parse_args()
  inputs  = args.input
  outputs = args.output
  mode    = args.directory_mode

  return inputs, outputs, mode


def _main():
  inputs, outputs, directory_mode = parse_args()
  svg2png = SVG2PNG()
  if not directory_mode:
    svg2png.convert(inputs, outputs)
  else:
    svg2png.convert_directory(inputs, outputs)


if __name__ == "__main__":
  _main()