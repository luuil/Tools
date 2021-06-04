#!/usr/bin/env python
# -*- coding: utf-8 -*-
# liulu@huya.com

"""
test video related operations.
"""
import logging
import os

import video_image_tool.video.misc as vmisc
import video_image_tool.image.misc as imisc
from video_image_tool import util


def create_videos():
    dir4 = 'output_symbol_test_holebody'
    imgs = ['00000']
    # imgs = [str(idx).zfill(5) for idx in range(7)]
    # types = ["P1_shenmihuaixiao"]
    types = ["Happy", "P0_haixiu", "P1_shenmihuaixiao", "Sad", "p0_paomeiyan", "p1_kunkun", "p1_shengqi"]

    dir_name = r'G:\projects\image_translation\cartoon_controllable\talking-head-anime-2-demo\data\output\hongyu'

    for im in imgs:
        for t in types:
            image_path = os.path.join(dir_name, dir4, im, t, 'withsymbol')
            images = imisc.list_images(image_path)

            video_path = os.path.join(dir_name, dir4, im, t, 'withsymbol', 'ts.mp4')
            vmisc.create_video(images, video_path, fps=10)


def concatenate_live2d_videos():
    dir1 = 'output_symbol_test'
    dir2 = 'output_symbol_test_withoutsymbol'
    dir3 = 'output_symbol_test_onlysymbol'
    dir4 = 'output_symbol_test_holebody'
    # imgs = ['00000']
    # imgs = [str(idx).zfill(5) for idx in range(7)]
    imgs = ['0'.zfill(5), '0'.zfill(5) + 'v2']
    # types = ["P1_shenmihuaixiao"]
    types = ["normal", "Happy", "P0_haixiu", "P1_shenmihuaixiao", "Sad", "p0_paomeiyan", "p1_kunkun", "p1_shengqi"]
    # types = ["Happy", "P0_haixiu", "P1_shenmihuaixiao", "Sad", "p0_paomeiyan", "p1_kunkun", "p1_shengqi"]

    dir_name = r'G:\projects\image_translation\cartoon_controllable\talking-head-anime-2-demo\data\output\hongyu'

    concatenate_videos = list()
    for im in imgs:
        videos = list()
        titles = list()
        for t in types:
            breathe_path = os.path.join(dir_name, dir4, im, t, 'breathe02', 'ts.mp4')
            videos.append(breathe_path)
            titles.append(t)

        output_path = os.path.join(dir_name, dir4, f'{im}_concatenate03.mp4')
        concatenate_videos.append(output_path)
        vmisc.concatenate_videos(
            videos,
            output_path,
            texts=titles,
            text_location=(0, .1),
        )
    vmisc.merge_videos(concatenate_videos, os.path.join(dir_name, dir4, f'all03.mp4'))


def merge_video():
    vpath2 = r'\\huya-luuil\liulu-results\cartoon_controllable\20210521\fake3d'
    vpath2 = r'G:\projects\image_translation\cartoon_controllable\talking-head-anime-2-demo\data\output\hongyu\output_symbol_test_holebody'
    vpath2 = r'\\huya-luuil\liulu-results\cartoon_controllable\20210604\release_alpha'
    videos = [
        'mengmei00016_v0.2.1_changtai.mp4',
        'mengmei00016_v0.2.1_baogou.mp4',
        'mengmei00016_v0.2.1_jianpan.mp4',
        'banshen00006_v0.1.0.mp4',
        'banshen00001_v0.1.0.mp4',
        'banshen00004_v0.1.0.mp4',
    ]
    titles = [name[:-10] for name in videos]
    # titles = [
    #     'video1_v0.0.4',
    #     'video2_v0.0.4',
    #     'video3_v0.0.4',
    #     'video4_v0.0.4',
    # ]
    videos = [os.path.join(vpath2, v) for v in videos]
    vmisc.merge_videos(
        videos,
        fr'{vpath2}/release_alpha.mp4',
        texts=titles,
        # grid_size=(1, len(videos)),
        grid_size=(2, 3),
        # text_location=(0, .95),
        text_location=(0, .1),
        nframes=None
    )


if __name__ == '__main__':
    util.set_default_logging()

    merge_video()
    # concatenate_live2d_videos()
    # create_videos()
    pass
