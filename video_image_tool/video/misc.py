#!/usr/bin/env python
# -*- coding: utf-8 -*-
# liulu@huya.com

"""
Miscellaneous utility functions for video operations.
"""
import logging
import os
from typing import Union, List

import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip

from video_image_tool.video.video_reader import VideoReader
import video_image_tool.image.misc as imisc


def merge_videos(videos_in, video_out, texts=None, grid_size=None, nframes: int = None, text_location=None):
    if texts is None:
        texts = [None] * len(videos_in)
    assert len(videos_in) == len(texts)

    if not os.path.exists(os.path.dirname(video_out)):
        os.makedirs(os.path.dirname(video_out), exist_ok=True)

    video_readers = [VideoReader(v) for v in videos_in]
    generators = [e.extract(text=t, text_location=text_location) for e, t in zip(video_readers, texts)]

    if nframes is not None:
        assert nframes > 0
        least_frames = nframes
    else:
        least_frames = sorted([e.total_frames for e in video_readers])[0]  # all with same number of frames

    least_size = sorted([e.size for e in video_readers])[0]  # all with same size WH

    # read one frame and resize for each generator, then get the output video size
    cur_frames = np.array([cv2.resize(next(g), least_size) for g in generators])
    frames_grid = imisc.create_image_grid(cur_frames, grid_size=grid_size)  # HWC

    fps = video_readers[0].fps  # use the fps of first video
    out_size = frames_grid.shape[0:2]  # HWC to HW
    out_size = out_size[::-1]  # reverse HW to WH, as VideoWriter need that format
    video_writer = cv2.VideoWriter(video_out,
                                   cv2.VideoWriter_fourcc(*'XVID'),
                                   fps,
                                   out_size)

    for n in range(least_frames-1):
        if n % 100 == 0:
            logging.info(f'{n}: {len(cur_frames)} frames merge into grid with size={frames_grid.shape}')
        video_writer.write(frames_grid)

        cur_frames = np.array([cv2.resize(next(g), least_size) for g in generators])
        frames_grid = imisc.create_image_grid(cur_frames, grid_size=grid_size)

    video_writer.release()
    logging.info(f'Output video saved... {video_out}')


def concatenate_videos(videos_in, video_out, texts=None, text_location=None):
    if texts is None:
        texts = [None] * len(videos_in)
    assert len(videos_in) == len(texts)

    if not os.path.exists(os.path.dirname(video_out)):
        os.makedirs(os.path.dirname(video_out), exist_ok=True)

    video_readers = [VideoReader(v) for v in videos_in]
    least_size = sorted([e.size for e in video_readers])[0]  # all with same size WH

    fps = video_readers[0].fps  # use the fps of first video
    video_writer = cv2.VideoWriter(video_out,
                                   cv2.VideoWriter_fourcc(*'XVID'),
                                   fps,
                                   least_size)

    logging.info(f'Writing out: {video_out}')
    for vr, vp, t in zip(video_readers, videos_in, texts):
        logging.info(f'\t{vp}')
        for frame in vr.extract(text=t, text_location=text_location):
            if vr.size != least_size:
                frame = cv2.resize(frame, least_size)
            video_writer.write(frame)

    video_writer.release()
    logging.info(f'Writing done: {video_out}')


def create_video(images: Union[np.ndarray, List[str]], video_out: str, fps=None, ismask=False):
    if isinstance(images, list):
        flag_load_image = True
    else:
        assert images.ndim == 3 or images.ndim == 4, f'only support 3 or 4 dimension inputs, now: {images.ndim}'
        flag_load_image = False

    logging.info(f'num of images to create video: {len(images)}')
    try:
        clip = ImageSequenceClip(images, fps=fps, ismask=ismask, load_images=flag_load_image)
        clip.write_videofile(video_out)
        clip.close()
    except Exception as e:
        logging.error(e)
    logging.info(f'saved video successful: {video_out}')
