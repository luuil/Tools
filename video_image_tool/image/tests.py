#!/usr/bin/env python
# -*- coding: utf-8 -*-
# liulu@huya.com

"""
test image related operations.
"""

import logging
import os
import sys

import video_image_tool.image.misc as imisc
from video_image_tool import util

sys.path.append('.')
sys.path.append('..')


def test_merge_images_dir():
    path = r"\\HUYA-LUUIL\liulu-results\cartoon_controllable\20210521\half"
    out = fr"{path}/merge.jpg"
    images = imisc.list_images(path)
    names = [os.path.basename(f)[:-4] for f in images]
    imisc.merge_images(images, out,
                       show=False,
                       titles=names,
                       text_location=(0, .1),
                       color=(0, 0, 255))


def concatenate_images():
    material_dir = r"G:\projects\0results\cartoon_controllable\20210604\materials\mengmei\res_all\00016"

    for scenery in os.listdir(material_dir):
        images = list()
        for expression in os.listdir(os.path.join(material_dir, scenery)):
            src_dir = os.path.join(material_dir, scenery, expression, "frames")
            images += imisc.list_images(src_dir)
        out = os.path.join(material_dir, scenery, "sprite.png")
        imisc.merge_images(images, out, show=False)


if __name__ == '__main__':
    util.set_default_logging()

    # test_merge_images_dir()
    concatenate_images()


