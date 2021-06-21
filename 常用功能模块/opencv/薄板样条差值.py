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

    # points = [[16, 152], [16, 210], [96, 89], [96, 168], [175, 39], [175, 143], [306, 23], [306, 107],
    #           [438, 9], [438, 113], [577, 53], [577, 132], [656, 87], [656, 171], [738, 132], [738, 240]]
    points = [[1, 162], [16, 152], [96, 89], [175, 39], [306, 23], [438, 9], [577, 53], [656, 87], [738, 132], [750, 241],
              [750, 243], [738, 240], [656, 171], [577, 132], [438, 113], [306, 107], [175, 143], [96, 168], [16, 210], [1, 170]]
    mask_img = np.zeros((img_h, img_w), dtype=np.uint8)
    cv2.polylines(mask_img, np.array([points]), True, 255, 1)
    source = []
    for index in range(img_w//25):
        cond = np.where(mask_img[:, index*25] == 255)
        if len(cond[0]) > 0:
            source.append([index*25, cond[0][0]])
            source.append([index*25, cond[0][-1]])
    # cv2.imshow('mask_img', mask_img)
    # cv2.waitKey()
    # source = [[16, 152], [16, 210]]
    for point in source:
        cv2.circle(image, tuple(point), 2, (0, 0, 255), 2)
    cv2.imshow('image', image)
    cv2.waitKey()
    source_h = abs(min(np.array(source)[:, 1]) - max(np.array(source)[:, 1]))
    source_w = abs(min(np.array(source)[:, 0]) - max(np.array(source)[:, 0]))
    text_len = np.sqrt(source_h * source_h + source_w * source_w)
    word_len = int(text_len / (len(source) // 2 - 1))
    target = []
    for i in range(len(source) // 2):
        target.append([i * word_len, 0])
        target.append([i * word_len, 32])

    out_img = tps_cv2(np.array(source), np.array(target), image)
    cv2.imshow('cut_img', out_img)
    cv2.imshow('out_cut_img', out_img[:32, :int(text_len)])
    cv2.waitKey()


if __name__ == '__main__':
    main()
