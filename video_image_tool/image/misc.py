#!/usr/bin/env python
# -*- coding: utf-8 -*-
# liulu@huya.com

"""
Miscellaneous utility functions for image operations.
"""

import os
import numpy as np
import cv2
import PIL.Image
import PIL.ImageDraw
import scipy


def read_by_pil(path, np_format=False, size=512):
    assert os.path.exists(path)
    pil_img = PIL.Image.open(path)
    pil_img = pil_img.resize((size, size))
    return np.array(pil_img) if np_format else pil_img


def read_by_cv(path, flags=cv2.IMREAD_UNCHANGED):
    assert os.path.exists(path)
    return cv2.imread(path, flags)


def adjust_dynamic_range(data, drange_in, drange_out):
    if drange_in != drange_out:
        scale = (np.float32(drange_out[1]) - np.float32(drange_out[0])) / (np.float32(drange_in[1]) - np.float32(drange_in[0]))
        bias = (np.float32(drange_out[0]) - np.float32(drange_in[0]) * scale)
        data = data * scale + bias
    return data


def create_image_grid(images, *args, grid_size=None, titles=None, loc_scale=None, color=None, **kwargs):
    _args, _kwargs = args, kwargs
    assert images.ndim == 3 or images.ndim == 4
    num, img_w, img_h = images.shape[0], images.shape[-2], images.shape[-3]

    if grid_size is not None:
        grid_h, grid_w = tuple(grid_size)
    else:
        grid_w = max(int(np.ceil(np.sqrt(num))), 1)
        grid_h = max((num - 1) // grid_w + 1, 1)

    if titles is not None:
        assert len(images) == len(titles)
        assert all([isinstance(t, str) for t in titles])

        if loc_scale is not None:
            w_scale, h_scale = loc_scale
        else:
            w_scale, h_scale = 1 / 3, 1 / 3

        if color is None:
            color = (255, 0, 0)

        for title, image in zip(titles, images):
            org = int(img_w * w_scale), int(img_h * h_scale)
            cv2.putText(image, title, org, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)

    grid = np.zeros([grid_h * img_h, grid_w * img_w] + list(images.shape[-1:]), dtype=images.dtype)
    for idx in range(num):
        x = (idx % grid_w) * img_w
        y = (idx // grid_w) * img_h
        grid[y: y + img_h, x: x + img_w, ...] = images[idx]
    return grid


def convert_to_pil_image(image, *args, drange=(0, 1), hwc_format=False, **kwargs):
    _args, _kwargs = args, kwargs
    assert image.ndim == 2 or image.ndim == 3
    if image.ndim == 3 and not hwc_format:
        if image.shape[0] == 1:
            image = image[0] # grayscale CHW => HW
        else:
            image = image.transpose(1, 2, 0) # CHW -> HWC

    image = adjust_dynamic_range(image, drange, [0, 255])
    image = np.rint(image).clip(0, 255).astype(np.uint8)
    fmt = ('RGBA' if image.shape[2] == 4 else 'RGB') if image.ndim == 3 else 'L'
    return PIL.Image.fromarray(image, fmt)


def save_image(image, filename, drange=[0,1], quality=95):
    img = convert_to_pil_image(image, drange)
    if '.jpg' in filename:
        img.save(filename,"JPEG", quality=quality, optimize=True)
    else:
        img.save(filename)


def save_image_grid(images, filename, *args, **kwargs):
    convert_to_pil_image(create_image_grid(images, *args, **kwargs), *args, **kwargs).save(filename)


def covert_pil_to_cv_image(image):
    """
    :param image: PIL image
    :return: cv2 image
    """
    pil_arr = np.array(image)
    return cv2.cvtColor(pil_arr, cv2.COLOR_RGB2BGR)


def merge_images(images_in, image_out, *args, **kwargs):
    images = []
    for v in images_in:
        images.append(read_by_cv(v))

    least_size = sorted([(img.shape[0], img.shape[1]) for img in images])[0]  # get least size WH
    images = np.array([cv2.resize(img, least_size) for img in images])  # resize to same size WH
    grid = create_image_grid(images, *args, **kwargs)
    cv2.imwrite(image_out, grid)


def ffhq_like_aligned_face(img, face_landmarks, scale_factor=1, transform_size_default=512, h_scale=2.0, v_scale=1.8, c_scale=0.1):
    """
    ref to: https://github.com/NVlabs/ffhq-dataset/blob/master/download_ffhq.py#L259
    and do some modify

    :return: aligned face
    """
    LEFT_EYE = (60, 68)
    RIGHT_EYE = (68, 76)
    MOUTH = (76, 88)
    MOUTH_CONNER = (0, 6)

    lm_eye_left = face_landmarks[LEFT_EYE[0]: LEFT_EYE[1]]  # left-clockwise
    lm_eye_right = face_landmarks[RIGHT_EYE[0]: RIGHT_EYE[1]]  # left-clockwise
    lm_mouth_outer = face_landmarks[MOUTH[0]: MOUTH[1]]  # left-clockwise
    mouth_left = lm_mouth_outer[MOUTH_CONNER[0]]
    mouth_right = lm_mouth_outer[MOUTH_CONNER[1]]

    # img_original_shape = img.shape
    # Calculate auxiliary vectors.
    eye_left = np.mean(lm_eye_left, axis=0)
    eye_right = np.mean(lm_eye_right, axis=0)
    eye_avg = (eye_left + eye_right) * 0.5  # 两眼中点坐标
    eye_to_eye = eye_right - eye_left  # 两眼x,y方向的距离

    mouth_avg = (mouth_left + mouth_right) * 0.5  # 嘴的中心坐标
    eye_to_mouth = mouth_avg - eye_avg  # 眼睛中点到嘴巴中点的x,y方向的距离

    # Choose oriented crop rectangle.
    x = eye_to_eye - np.flipud(eye_to_mouth) * [-1, 1]
    x /= np.hypot(*x)
    x *= max(np.hypot(*eye_to_eye) * h_scale, np.hypot(*eye_to_mouth) * v_scale)
    x = x.astype(np.float32)
    y = np.flipud(x) * [-1, 1]
    y = y.astype(np.float32)
    c = eye_avg + eye_to_mouth * c_scale
    quad = np.stack([c - x - y, c - x + y, c + x + y, c + x - y])
    qsize = np.hypot(*x) * np.float32(2)

    # Crop.
    border = max(int(np.rint(qsize * 0.1)), 3)
    crop = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(np.ceil(max(quad[:, 0]))), int(np.ceil(max(quad[:, 1]))))
    crop = (max(int((crop[0] - border) / scale_factor + 0.5) * scale_factor, 0),
            max(int((crop[1] - border) / scale_factor + 0.5) * scale_factor, 0),
            min(int((crop[2] + border) / scale_factor + 0.5) * scale_factor, img.shape[1]),
            min(int((crop[3] + border) / scale_factor + 0.5) * scale_factor, img.shape[0]))

    if crop[2] - crop[0] < img.shape[1] or crop[3] - crop[1] < img.shape[0]:
        cropimage = img[crop[1]:crop[3], crop[0]:crop[2]].copy()
        quad -= crop[0:2]
    else:
        cropimage = img.copy()

    # crop_lefttop_point = np.matrix([crop[0], crop[1]])  # used for align src landmarks

    transform_size = transform_size_default

    pts2 = np.float32([[0, 0], [transform_size - 1, 0], [0, transform_size - 1]])
    pts1 = np.float32([[quad[0, 0], quad[0, 1]], [quad[3, 0], quad[3, 1]], [quad[1, 0], quad[1, 1]]])
    M_affine = cv2.getAffineTransform(pts1, pts2)

    warpimg = cv2.warpAffine(np.array(cropimage), M_affine, (transform_size, transform_size))

    return warpimg


def ffhq_aligned_face(img, lm, output_size=1024, transform_size=4096, enable_padding=True, h_scale=2.0, v_scale=1.8, c_scale=0.1):
    """
    https://github.com/NVlabs/ffhq-dataset/blob/master/download_ffhq.py#L259

    :param img: ndarray
    :param lm:
    :param output_size:
    :param transform_size:
    :param enable_padding:
    :param h_scale:
    :param v_scale:
    :param c_scale:
    :return:
    """

    # Parse landmarks: ld98 landmarks
    # pylint: disable=unused-variable
    lm_eye_left = lm[60: 68]  # left-clockwise
    lm_eye_right = lm[68: 76]  # left-clockwise
    lm_mouth_outer = lm[76: 88]  # left-clockwise

    # Calculate auxiliary vectors.
    eye_left = np.mean(lm_eye_left, axis=0)
    eye_right = np.mean(lm_eye_right, axis=0)
    eye_avg = (eye_left + eye_right) * 0.5
    eye_to_eye = eye_right - eye_left
    mouth_left = lm_mouth_outer[0]
    mouth_right = lm_mouth_outer[6]
    mouth_avg = (mouth_left + mouth_right) * 0.5
    eye_to_mouth = mouth_avg - eye_avg

    # Choose oriented crop rectangle.
    x = eye_to_eye - np.flipud(eye_to_mouth) * [-1, 1]
    x /= np.hypot(*x)
    x *= max(np.hypot(*eye_to_eye) * h_scale, np.hypot(*eye_to_mouth) * v_scale)
    y = np.flipud(x) * [-1, 1]
    c = eye_avg + eye_to_mouth * c_scale
    quad = np.stack([c - x - y, c - x + y, c + x + y, c + x - y])
    qsize = np.hypot(*x) * 2

    img = PIL.Image.fromarray(img)

    # Shrink.
    shrink = int(np.floor(qsize / output_size * 0.5))
    if shrink > 1:
        rsize = (int(np.rint(float(img.size[0]) / shrink)), int(np.rint(float(img.size[1]) / shrink)))
        img = img.resize(rsize, PIL.Image.ANTIALIAS)
        quad /= shrink
        qsize /= shrink

    # Crop.
    border = max(int(np.rint(qsize * 0.1)), 3)
    crop = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(np.ceil(max(quad[:, 0]))),
            int(np.ceil(max(quad[:, 1]))))
    crop = (max(crop[0] - border, 0), max(crop[1] - border, 0), min(crop[2] + border, img.size[0]),
            min(crop[3] + border, img.size[1]))
    if crop[2] - crop[0] < img.size[0] or crop[3] - crop[1] < img.size[1]:
        img = img.crop(crop)
        quad -= crop[0:2]

    # Pad.
    pad = (int(np.floor(min(quad[:, 0]))), int(np.floor(min(quad[:, 1]))), int(np.ceil(max(quad[:, 0]))),
           int(np.ceil(max(quad[:, 1]))))
    pad = (max(-pad[0] + border, 0), max(-pad[1] + border, 0), max(pad[2] - img.size[0] + border, 0),
           max(pad[3] - img.size[1] + border, 0))
    if enable_padding and max(pad) > border - 4:
        pad = np.maximum(pad, int(np.rint(qsize * 0.3)))
        img = np.pad(np.float32(img), ((pad[1], pad[3]), (pad[0], pad[2]), (0, 0)), 'reflect')
        h, w, _ = img.shape
        y, x, _ = np.ogrid[:h, :w, :1]
        mask = np.maximum(1.0 - np.minimum(np.float32(x) / pad[0], np.float32(w - 1 - x) / pad[2]),
                          1.0 - np.minimum(np.float32(y) / pad[1], np.float32(h - 1 - y) / pad[3]))
        blur = qsize * 0.02
        img += (scipy.ndimage.gaussian_filter(img, [blur, blur, 0]) - img) * np.clip(mask * 3.0 + 1.0, 0.0, 1.0)
        img += (np.median(img, axis=(0, 1)) - img) * np.clip(mask, 0.0, 1.0)
        img = PIL.Image.fromarray(np.uint8(np.clip(np.rint(img), 0, 255)), 'RGB')
        quad += pad[:2]

    # Transform.
    img = img.transform((transform_size, transform_size), PIL.Image.QUAD, (quad + 0.5).flatten(),
                        PIL.Image.BILINEAR)
    if output_size < transform_size:
        img = img.resize((output_size, output_size), PIL.Image.ANTIALIAS)

    return np.array(img)


def list_images(p, filters=()):
    assert os.path.exists(p)
    images = [name for name in os.listdir(p)]

    filters = list(filters)
    filters.insert(0, lambda x: x[-3:] in ('jpg', 'png'))
    for filter_cond in filters:
        images = filter(filter_cond, images)

    images = sorted(images)
    images = [os.path.join(p, name) for name in images]
    return images


