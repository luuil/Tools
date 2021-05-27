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


def create_video():
    image_path = r'../data/image'
    images = imisc.list_images(image_path)
    video_path = os.path.join(image_path, 'video.mp4')
    vmisc.create_video(images, video_path, fps=10)


def concatenate_videos():
    vpath = r'../data/video'
    videos = [
        "x.mp4",
        "x_copy.mp4",
        "x_copy1.mp4",
    ]
    titles = [name[:-4] for name in videos]
    videos = [os.path.join(vpath, v) for v in videos]
    vmisc.concatenate_videos(
        videos,
        fr'{vpath}/concatenate.mp4',
        texts=titles,
        text_location=(0, 0.1))


def merge_video():
    vpath = r'../data/video'
    videos = [
        "x.mp4",
        "x_copy.mp4",
        "x_copy1.mp4",
    ]
    titles = [name[:-4] for name in videos]
    videos = [os.path.join(vpath, v) for v in videos]
    vmisc.merge_videos(
        videos,
        fr'{vpath}/merge.mp4',
        texts=titles,
        grid_size=(2, 2),
        text_location=(.3, .95),
        nframes=None
    )


if __name__ == '__main__':
    log_fmt = '%(asctime)s|%(levelname)s|%(filename)s@%(funcName)s(%(lineno)d): %(message)s'
    logging.basicConfig(format=log_fmt, level=logging.DEBUG)

    merge_video()
    # create_video()
    # concatenate_videos()
    pass
