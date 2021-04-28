# coding: utf-8
# author: luuil@outlook.com
# created: 2020-07-02 10:57:22
# modified: 2020-07-02 10:58:00
# =============================================================
r"""deduplication images brute force"""

from abc import ABC, abstractmethod
import numpy as np
import cv2
import os


class Deduplication(ABC):
    def __init__(self):
        super(Deduplication, self).__init__()

    @staticmethod
    @abstractmethod
    def distance(img1: np.ndarray, img2: np.ndarray) -> float:
        pass

    @staticmethod
    def read_img(img_path, gray=False, show=False):
        assert os.path.exists(img_path)
        read_flag = cv2.IMREAD_UNCHANGED if not gray else cv2.IMREAD_GRAYSCALE
        img = cv2.imread(img_path, read_flag)
        if img is None:
            raise TypeError(f'{img_path} is not image')
        if show:
            cv2.imshow(img_path, img)
            cv2.waitKey(0)
        return img


class PixelDeduplication(Deduplication):
    @staticmethod
    def distance(img1, img2):
        """pixel distance"""
        assert img2.shape == img2.shape
        return np.mean(np.abs(img1 - img2))


def deduplicate():
    idir = r'G:\data\ffhq_yellow_512x512_douyin_cartoon\src\20200706zb\mate30pro'
    # idir = r'G:\data\ffhq_yellow_512x512_douyin_cartoon\src\20200706zb\mi9'
    # idir = r'G:\data\ffhq_yellow_512x512_douyin_cartoon\src\20200706zb\1plus7pro'
    nlist = sorted(os.listdir(idir))
    print(nlist)
    ilist = [os.path.join(idir, name) for name in nlist]
    n_img = len(ilist)

    pd = PixelDeduplication()

    def test_thresh():
        img0 = pd.read_img(ilist[0], gray=True, show=True)
        img1 = pd.read_img(ilist[1], gray=True, show=True)
        img2 = pd.read_img(ilist[2], gray=True, show=True)
        img4 = pd.read_img(ilist[4], gray=True, show=True)
        img6 = pd.read_img(ilist[6], gray=True, show=True)
        cv2.waitKey(0)
        d00 = pd.distance(img0, img0)
        d01 = pd.distance(img0, img1)
        d02 = pd.distance(img0, img2)
        d04 = pd.distance(img0, img4)
        d26 = pd.distance(img2, img6)
        print(d00, d01, d02, d04, d26)

    # test_thresh()

    def process_all():
        MAX_DEPULICATE = 1
        DIST_THRESH = 70
        STEP = 2
        SEARCH_RANGE = 8*STEP
        # SEARCH_RANGE = n_img

        idx_list = list(range(n_img))
        for i in range(0, n_img, STEP):
            if i > idx_list[i]:
                print(f'continue: {i, idx_list[i]}')
                continue
            imga = pd.read_img(ilist[i], gray=True)
            n_depucate = 0

            limit = n_img if i+SEARCH_RANGE > n_img else i+SEARCH_RANGE
            for j in range(i+2, limit, STEP):
                imgb = pd.read_img(ilist[j], gray=True)
                dist = pd.distance(imga, imgb)
                print(i, j, dist)
                if dist <= DIST_THRESH:

                    idx_list[j] = i
                    if j+1 < n_img:
                        idx_list[j+1] = i

                    n_depucate += 1
                    if n_depucate >= MAX_DEPULICATE:
                        print(f'break j={j}')
                        break

        print(idx_list)
        unique = list(set(idx_list))
        print(len(unique), unique)
        return unique

    def copy_to(unique_list, tgt_dir):
        os.makedirs(tgt_dir, exist_ok=True)
        import shutil

        for idx in unique_list:
            shutil.copy(ilist[idx], os.path.join(tgt_dir, nlist[idx]))

    unique_list = process_all()
    copy_to(unique_list, r'G:\data\ffhq_yellow_512x512_douyin_cartoon\pre-ready\mate30pro-20200706')
    # copy_to(unique_list, r'G:\data\ffhq_yellow_512x512_douyin_cartoon\pre-ready\mi9-20200706')
    # copy_to(unique_list, r'G:\data\ffhq_yellow_512x512_douyin_cartoon\pre-ready\1plus7pro-20200706')


if __name__ == "__main__":
    deduplicate()
