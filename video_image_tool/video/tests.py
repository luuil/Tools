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
    vpath2 = r'\\HUYA-LUUIL\liulu-results\cartoon_controllable\20210604'
    videos = [
        'memgmei00002_v0.2.1.mp4',
        'memgmei00002_v0.2.1_baogou.mp4',
        'memgmei00002_v0.2.1_jianpan.mp4',
    ]
    titles = None
    # titles = [name[:-10] for name in videos]
    # titles = [
    #     'video1_v0.0.4',
    #     'video2_v0.0.4',
    #     'video3_v0.0.4',
    #     'video4_v0.0.4',
    # ]
    videos = [os.path.join(vpath2, v) for v in videos]
    vmisc.merge_videos(
        videos,
        fr'{vpath2}/mengmei00002_v0.2.1_merge.mp4',
        texts=titles,
        # grid_size=(1, len(videos)),
        grid_size=(3, 1),
        # text_location=(0, .95),
        text_location=(0, .1),
        nframes=None
    )


def extract_vap_video():
    """
    https://github.com/Tencent/vap
    :return: None
    """
    import cv2
    from video_image_tool.video.video_reader import VideoReader

    vap_dir = r'G:\projects\0results\cartoon_controllable\anime_material\mengmei\res_vap_v3_breast418-7002\breast418-7002-seed1115\changtai\default\vap_watermark2'
    jpath = os.path.join(vap_dir, 'vap.json')
    vpath = os.path.join(vap_dir, 'vap.mp4')
    fpath = os.path.join(vap_dir, 'vap_frames')
    os.makedirs(fpath, exist_ok=True)

    json = util.json_load(jpath)['info']
    vr = VideoReader(vpath)
    idx = 0
    for frame in vr.extract():
        x, y, w, h = json['rgbFrame']
        w_dst, h_dst = w, h
        bgr = frame[y:y + h, x:x + w, :]

        x, y, w, h = json['aFrame']
        alpha = frame[y:y + h, x:x + w, 0]
        # alpha[alpha > 0] = 255
        alpha = cv2.resize(alpha, (w_dst, h_dst))

        bgra = cv2.merge((bgr, alpha))
        cv2.imwrite(os.path.join(fpath, f'{idx}.png'), bgra)
        idx += 1


if __name__ == '__main__':
    util.set_default_logging()

    # merge_video()
    # concatenate_live2d_videos()
    # create_videos()
    extract_vap_video()

    # images = imisc.list_images(r'\\HUYA-LUUIL\liulu-results\cartoon_controllable\anime_material\banshen\res_vap_v2\00000\changtai\default\vap_watermark\vap_frames')
    # vmisc.create_video(images, r'\\HUYA-LUUIL\liulu-results\cartoon_controllable\anime_material\banshen\res_vap_v2\00000\changtai\default\vap_watermark\vap_frames\vap.mp4', withmask=True)
    pass
