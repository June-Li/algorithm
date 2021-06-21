# import random

# a = [11, 25]
# for i in range(99):
#     b = random.randint(0, len(a))
#     print(b)

# for i in range(100):
#     a = random.randint(0, 100)
#     print(a)

# import cv2
# import os
# import numpy as np
#
# image = cv2.imread('/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/SSL_yolov3_FixMatch/buffer/a.jpg')
# # line = '0 0.5 0.28359 0.5011 0.20781'
# line = '[          0      47.601      89.157      379.14      177.34]'
# line = line.strip('[').strip(']').split(' ')
# line = [i for i in line if i != '']
# # line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
# # [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
# # x_0 = int((x_center - weight / 2) * np.shape(image)[1])
# # y_0 = int((y_center - height / 2) * np.shape(image)[0])
# # x_1 = int((x_center + weight / 2) * np.shape(image)[1])
# # y_1 = int((y_center + height / 2) * np.shape(image)[0])
# # cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=2)
# # cv2.imshow('image', image)
# # cv2.waitKey()
#
# [x_0, y_0, x_1, y_1] = [int(float(i)) for i in line[1:]]
# cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=2)
# cv2.imshow('image', image)
# cv2.waitKey()

# import math
# a = math.atan()
# print(a)


import cv2
import numpy as np
from math import fabs, sin, cos, radians
from scipy.stats import mode


# def warpAffine_img(img, degree=45, filled_color=-1):
#     """
#     Desciption:
#             Get img rotated a certain degree,
#         and use some color to fill 4 corners of the new img.
#     """
#
#     # 获取旋转后4角的填充色
#     if filled_color == -1:
#         filled_color = mode([img[0, 0], img[0, -1],
#                              img[-1, 0], img[-1, -1]]).mode[0]
#     if np.array(filled_color).shape[0] == 2:
#         if isinstance(filled_color, int):
#             filled_color = (filled_color, filled_color, filled_color)
#     else:
#         filled_color = tuple([int(i) for i in filled_color])
#
#     height, width = img.shape[:2]
#
#     # 旋转后的尺寸
#     height_new = int(width * fabs(sin(radians(degree))) +
#                      height * fabs(cos(radians(degree))))
#     width_new = int(height * fabs(sin(radians(degree))) +
#                     width * fabs(cos(radians(degree))))
#
#     mat_rotation = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)
#
#     mat_rotation[0, 2] += (width_new - width) / 2
#     mat_rotation[1, 2] += (height_new - height) / 2
#
#     # Pay attention to the type of elements of filler_color, which should be
#     # the int in pure python, instead of those in numpy.
#     img_rotated = cv2.warpAffine(img, mat_rotation, (width_new, height_new),
#                                  borderValue=filled_color)
#     # 填充四个角
#     mask = np.zeros((height_new + 2, width_new + 2), np.uint8)
#     mask[:] = 0
#     seed_points = [(0, 0), (0, height_new - 1), (width_new - 1, 0),
#                    (width_new - 1, height_new - 1)]
#     for i in seed_points:
#         cv2.floodFill(img_rotated, mask, i, filled_color)
#
#     return img_rotated
#
#
# img_ori = cv2.imread('/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/poc/xmpoc/src/PaddleOCR/doc/my_imgs_15/0416_1.jpg')
# img_h, img_w, _ = np.shape(img_ori)
# img_show_1 = img_ori.copy()
# cv2.circle(img_show_1, (img_w//2, img_h//2), 2, (0, 0, 255), 2)
# cv2.imshow('show_1', img_show_1)
#
# img_rot = warpAffine_img(img_ori.copy(), -45)
# img_h, img_w, _ = np.shape(img_rot)
# cv2.circle(img_rot, (img_w//2, img_h//2), 2, (0, 0, 255), 2)
# cv2.imshow('img_rot', img_rot)
# cv2.waitKey()

# import math
# print(math.degrees(math.atan(10/1330)))
# print(math.degrees(math.atan(10/10)))
# def fun(my_list):
#     if type(my_list).__name__ != 'list':
#         print(my_list)
#         return
#     for i in my_list:
#         fun(i)
# my_list = [1, [5, 9], [4, [6, [2, 1, 8]]]]
# fun(my_list)

def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


print(longestCommonSubsequence('我叫李俊吗', '叫吗'))
