import cv2
import numpy as np
import time


def tps_cv2(source, target, img):
    """
    使用cv2自带的tps处理
    """
    tps = cv2.createThinPlateSplineShapeTransformer()

    source_cv2 = source.reshape(1, -1, 2)
    target_cv2 = target.reshape(1, -1, 2)

    matches = list()
    for i in range(0, len(source_cv2[0])):
        matches.append(cv2.DMatch(i, i, 0))

    tps.estimateTransformation(target_cv2, source_cv2, matches)
    new_img_cv2 = tps.warpImage(img)

    return new_img_cv2


def main():
    image = cv2.imread('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_19/cu.png')
    img_h, img_w, _ = np.shape(image)
    cv2.imshow('image', image)

    source = [[16, 152], [16, 210], [96, 89], [96, 168], [175, 39], [175, 143], [306, 23], [306, 107],
              [438, 9], [438, 113], [577, 53], [577, 132], [656, 87], [656, 171], [738, 132], [738, 240]]
    target = []
    for i in range(len(source) // 2):
        target.append([i * 90, 0])
        target.append([i * 90, 32])

    start = time.time()
    source, target = np.array(source), np.array(target)
    print('use time: ', time.time() - start)

    out_img = tps_cv2(source, target, image)
    cv2.imshow('cut_img', out_img)
    cv2.imshow('out_cut_img', out_img[:35, :630])
    cv2.waitKey()


if __name__ == '__main__':
    main()
