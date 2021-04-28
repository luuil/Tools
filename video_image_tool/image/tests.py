#!/usr/bin/env python
# -*- coding: utf-8 -*-
# liulu@huya.com

"""
test image related operations.
"""

import os
import sys

import video_image_tool.image.misc as imisc

sys.path.append('.')
sys.path.append('..')


def test_merge_images_dir():
    path, out = r"../data/image", r"../data/merge.png"
    images = imisc.list_images(path)
    names = [os.path.basename(f)[:-4] for f in images]
    imisc.merge_images(images, out, titles=names, loc_scale=(.5, .9), color=(255, 0, 0))


if __name__ == '__main__':
    test_merge_images_dir()
