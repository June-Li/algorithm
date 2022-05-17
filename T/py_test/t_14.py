import os
import shutil
import numpy as np
import cv2

# base_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/v1-/un_labels/train/'
# image_name_list = os.listdir(base_path)
# count = 0
# for image_name in image_name_list:
#     if image_name.startswith('baidu') or image_name.startswith('sougou'):
#         count += 1
#         os.remove(base_path + image_name)
# print('total: ', count)

# image = np.zeros((500, 500), dtype=np.uint8)
# image[100:150, 100:400] = 255
# image[100:400, 100:150] = 255
# image[300:400, 300:400] = 255
# cv2.imshow('image', image)
# contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# contours_img = np.stack((image, image, image), -1)
# cv2.polylines(contours_img, contours, True, (0, 0, 255), 4)
# cv2.imshow('contours img', contours_img)
# print(contours)
# cv2.waitKey()

import torch

A = torch.ones(2, 3)  # 2x3的张量（矩阵）
D = 2 * torch.ones(3, 3)  # 2x4的张量（矩阵）
C = torch.cat((A, D), 1)  # 按维数1（列）拼接
print(C)
