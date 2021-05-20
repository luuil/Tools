#!/usr/bin/env python
# -*- coding: utf-8 -*-
# liulu@huya.com

"""
Miscellaneous utility functions for video operations.
"""

import os
import cv2
import numpy as np

from video_image_tool.video.extractvideo import ExtractFromVideo
import video_image_tool.image.misc as imisc


def merge_videos(videos_in, video_out, texts=None, grid_size=None, nframes: int = None, text_location=None):
    if texts is None:
        texts = [None] * len(videos_in)
    assert len(videos_in) == len(texts)

    if not os.path.exists(os.path.dirname(video_out)):
        os.makedirs(os.path.dirname(video_out), exist_ok=True)

    video_handles = []
    for v, text in zip(videos_in, texts):
        assert os.path.exists(v), f'{v} not exists!'
        video_handles.append((ExtractFromVideo(v), text))

    if nframes is not None:
        assert nframes > 0
        least_frames = nframes
    else:
        least_frames = sorted([e.total_frames for e, _t in video_handles])[0]  # all with same number of frames

    least_size = sorted([e.size for e, _t in video_handles])[0]  # all with same size WH
    generators = [e.extract(text=t, text_location=text_location) for e, t in video_handles]

    # read one frame and resize for each generator, then get the output video size
    cur_frames = np.array([cv2.resize(next(g), least_size) for g in generators])
    frames_grid = imisc.create_image_grid(cur_frames, grid_size=grid_size)  # HWC

    fps = video_handles[0][0].fps  # use the fps of first video
    out_size = frames_grid.shape[0:2]  # HWC to HW
    out_size = out_size[::-1]  # reverse HW to WH, as VideoWriter need that format
    video_writer = cv2.VideoWriter(video_out,
                                   cv2.VideoWriter_fourcc(*'XVID'),
                                   fps,
                                   out_size)

    for n in range(least_frames-1):
        if n % 100 == 0:
            print(f'{n}: {len(cur_frames)} frames merge into grid with size={frames_grid.shape}')
        video_writer.write(frames_grid)

        cur_frames = np.array([cv2.resize(next(g), least_size) for g in generators])
        frames_grid = imisc.create_image_grid(cur_frames, grid_size=grid_size)

    video_writer.release()
    print(f'Output video saved... {video_out}')
