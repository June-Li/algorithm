import os
import cv2
import numpy as np
from tqdm import tqdm

base_path = '/Volumes/my_disk/company/sensedeal/dataset/去印章/206/seal/'
img_name_list = os.listdir(base_path)
for idx, img_name in enumerate(tqdm(img_name_list)):
    # img_bgr = cv2.imread(base_path + img_name)

    # img_b = img_bgr[:, :, 0].copy()
    # img_g = img_bgr[:, :, 1].copy()
    # img_r = img_bgr[:, :, 2].copy()
    #
    # img_seal = np.zeros(np.shape(img_bgr), dtype=np.uint8)
    #
    # up, down = 210, 210
    # img_seal[np.stack((img_bgr[:, :, 0] < down, img_bgr[:, :, 1] < down, img_bgr[:, :, 2] > up), -1).all(-1)] = 255
    # cv2.putText(img_seal, str(np.sum(img_seal != 0)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
    #
    # cv2.imshow('img_bgr', img_bgr)
    # cv2.imshow('img_r', img_r)
    # cv2.imshow('img_seal', img_seal)
    #
    # cv2.waitKey()

    img = cv2.imread(base_path + img_name)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower_blue = np.array([100, 30, 100])
    upper_blue = np.array([150, 255, 255])

    mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

    res = cv2.bitwise_and(img, img, mask=mask)
    r, g, b = cv2.split(res)
    r_num = 0
    for i in b:
        for j in i:
            if j > 170:
                r_num += 1
    if (r_num > 30):
        cv2.putText(res, 'yes', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
    else:
        cv2.putText(res, 'no', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
    cv2.imshow('img', img)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    cv2.waitKey(0)
