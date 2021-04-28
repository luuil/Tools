#!/usr/bin/env python
# -*- coding: utf-8 -*-
# liulu@huya.com

"""
test video related operations.
"""

import os
import video_image_tool.video.misc as vmisc


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
        fr'{vpath}/.mp4',
        texts=titles,
        grid_size=(2, 2),
        loc_scale=(.3, .95),
        nframes=None
    )


if __name__ == '__main__':
    merge_video()
    pass
