#!/usr/bin/env python
# -*- coding: utf-8 -*-
# liulu@huya.com

"""
Extract images from video by OpenCV.
"""
import logging
import os
import cv2


class VideoReader(object):
    def __init__(self, path, frame_range=None, debug=False):
        self._vc = None

        assert os.path.exists(path), f'not exists: {path}'
        vc = cv2.VideoCapture(path)
        self._vc = vc

        self.size = int(self._vc.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self._vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self._vc.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(self._vc.get(cv2.CAP_PROP_FRAME_COUNT))

        self._start = 0
        self._count = self.total_frames

        self._debug = debug

        if frame_range is not None:
            self.set_frames_range(frame_range)

        if self._debug:
            logging.debug(f"video size( W x H ) : {self.size[0]} x {self.size[1]}")

    def __del__(self):
        self.release()

    def set_frames_range(self, frame_range=None):
        if frame_range is None:
            self._start = 0
            self._count = self.total_frames
        else:
            assert isinstance(frame_range, (list, tuple, range))
            if isinstance(frame_range, (list, tuple)):
                assert len(frame_range) == 2

            start, end = frame_range[0], frame_range[-1]
            if end is None \
                    or end == -1 \
                    or end >= self.total_frames:
                end = self.total_frames
            assert end >= start

            self._start = start
            self._count = end - start
            assert self._count <= self.total_frames

        self._vc.set(cv2.CAP_PROP_POS_FRAMES, self._start)

    def extract(self, path=None, bgr2rgb=False, target_size=None, text=None, text_location=None):
        if path is not None and not os.path.exists(path):
            os.makedirs(path)

        for i in range(0, self._count):
            success, frame = self._vc.read()
            if not success:
                logging.debug(f"index {i} exceeded.")
                break
            if self._debug:
                logging.debug(f"frame {self._start + i}")
            if path is not None:
                cv2.imwrite(os.path.join(path, f"{self._start + i}.jpg"), frame)
            if bgr2rgb:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if target_size is not None:
                assert len(target_size) == 2
                assert isinstance(target_size, (list, tuple))
                frame = cv2.resize(frame, tuple(target_size))
            if text is not None:
                if text_location is not None:
                    w_scale, h_scale = text_location
                    assert 0 <= w_scale <= 1.0 and 0 <= h_scale <= 1.0, "value range should be in [0.0, 1.0]"
                else:
                    w_scale, h_scale = 1 / 10, 1 / 10
                pos = int(self.size[0] * w_scale), int(self.size[1] * h_scale)  # text position
                frame = cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), thickness=1)
            yield frame

    def release(self):
        if self._vc is not None:
            self._vc.release()


if __name__ == "__main__":
    log_fmt = '%(asctime)s|%(levelname)s|%(filename)s@%(funcName)s(%(lineno)d): %(message)s'
    logging.basicConfig(format=log_fmt, level=logging.DEBUG)

    e = VideoReader("../data/video/x.mp4", (5, 10), debug=True)

    e.set_frames_range((1, 3))
    for image in e.extract("../extract_images"):
        logging.info(f"{image is not None}: {image.shape}")

    e.set_frames_range((3, 4))
    for image in e.extract():
        logging.info(f"{image is not None}: {image.shape}")
