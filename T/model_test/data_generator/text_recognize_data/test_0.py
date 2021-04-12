import os
import numpy as np
import sys
import cv2
import time
import random
# file = open('./info.txt')
# # lines = file.readlines()
# # for line in lines:
# #     print(line)
# #     time.sleep(99999)
# info_list = [part.strip().replace('\t', '') for part in file.readlines()]
# info_str = ''.join(info_list)
# print(info_str)
# cv2.imshow('image', np.array(np.zeros((4, 4), dtype=np.uint8), dtype=np.uint8))
# cv2.waitKey()

# def crop(Img):
#     H, W, z = Img.shape
#     y = H / 2 + 20
#     x = W / 2 + 60
#     winW = random.randrange(100, x - 60)
#     winH = random.randrange(80, y - 20)
#     cropImg = Img[int(y - winH):int(y + winH), int(x - winW):int(x + winW), :]
#
#     return cropImg
#
# image = cv2.imread('/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/data_generator/Generate_tables/img/H2_AN202003161376296621_1/49.jpg')
# print(np.shape(image))
# print(list(map(int, '1 2 3 4')))

# 矩形旋转示例
# import math
#
# image = np.zeros((1000, 1000, 3), dtype=np.uint8)
# pts = [[300, 300], [300, 700], [700, 700], [700, 300]]
# image = cv2.polylines(image, np.array([pts]), True, (0, 0, 255), 5)
# new_pts = []
# new_box = []
# theta = math.radians(30)
# for pt in pts:
#     [x, y] = pt
#     center_x, center_y = 500, 500
#     new_x = (x - center_x) * math.cos(theta) - (y - center_y) * math.sin(theta) + center_x - 100
#     new_y = (x - center_x) * math.sin(theta) + (y - center_y) * math.cos(theta) + center_y - 100
#     new_pts.append([int(new_x), int(new_y)])
# new_box.append([min(new_pts[0][0], new_pts[1][0], new_pts[2][0], new_pts[3][0]),
#                 min(new_pts[0][1], new_pts[1][1], new_pts[2][1], new_pts[3][1]),
#                 max(new_pts[0][0], new_pts[1][0], new_pts[2][0], new_pts[3][0]),
#                 max(new_pts[0][1], new_pts[1][1], new_pts[2][1], new_pts[3][1])])
# image = image[100:, 100:]
# image = cv2.polylines(image, np.array([new_pts]), True, (0, 255, 255), 5)
# image = cv2.rectangle(image, (new_box[0][0], new_box[0][1]), (new_box[0][2], new_box[0][3]), (255, 255, 255), 5)
# cv2.imshow('image', image)
# print(np.shape(image))
# cv2.waitKey()

import cv2
import numpy as np

# image = cv2.imread('/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/CRNN/yolov3/data/images/1-1.jpg')
# image = np.array(image)
# print(np.shape(image))

# pts = [[248, 711],
#        [437, 573],
#        [468, 614],
#        [279, 752]],
# pts = [[120, 357],
#        [131, 357],
#        [131, 382],
#        [120, 382]]
# pts = [[[120., 357.],
#         [131., 357.],
#         [131., 382.],
#         [120., 382.]],
#        [[299., 349.],
#         [424., 254.],
#         [455., 294.],
#         [330., 389.]],
#        [[86., 388.],
#         [103., 388.],
#         [103., 412.],
#         [86., 412.]],
#        [[495., 380.],
#         [599., 309.],
#         [623., 345.],
#         [519., 416.]],
#        [[540., 554.],
#         [611., 530.],
#         [629., 576.],
#         [557., 601.]],
#        [[155., 570.],
#         [161., 570.],
#         [161., 575.],
#         [155., 575.]],
#        [[491., 676.],
#         [569., 630.],
#         [587., 658.],
#         [508., 704.]],
#        [[248., 711.],
#         [437., 573.],
#         [468., 614.],
#         [279., 752.]],
#        [[290., 831.],
#         [456., 708.],
#         [484., 746.],
#         [318., 869.]]]
# pts = np.array(pts, dtype=np.int)
# image = np.zeros((1000, 1000, 3), dtype=np.uint8)
# image = cv2.polylines(image, np.array(pts), True, (0, 255, 255), 5)
# cv2.imshow('image', image)
# cv2.waitKey()

# image = np.zeros((1000, 1000, 3), dtype=np.uint8)
# mask = np.zeros((400, 100, 3), dtype=np.uint8)
# points = np.array([[0, 0], [100, 0], [100, 400], [0, 400]])
# img_crop_width = int(
#     max(
#         np.linalg.norm(points[0] - points[1]),
#         np.linalg.norm(points[2] - points[3])))
# img_crop_height = int(
#     max(
#         np.linalg.norm(points[0] - points[3]),
#         np.linalg.norm(points[1] - points[2])))
# pts_std = np.float32([[0, 0], [img_crop_width, 0],
#                       [img_crop_width, img_crop_height],
#                       [0, img_crop_height]])
# pts_std = np.array(pts_std, dtype=np.int)
# M = cv2.getPerspectiveTransform(points, pts_std)
# image = cv2.polylines(image, np.array([points]), True, (0, 255, 255), 5)
# image = cv2.polylines(image, np.array([pts_std]), True, (0, 0, 255), 5)
# dst_img = cv2.warpPerspective(
#             mask,
#             M, (img_crop_width, img_crop_height),
#             borderMode=cv2.BORDER_REPLICATE,
#             flags=cv2.INTER_CUBIC)
# cv2.imshow('image', image)
# cv2.imshow('mask', mask)
# cv2.imshow('dst img', dst_img)
# cv2.waitKey()
from PIL import Image
import torchvision.transforms as transforms

#coding=utf-8
# base_path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/pytorch-cifar100/data/test_img/1/'
# image_name_list = os.listdir(base_path)
# for image_name in image_name_list:
#     img_pil = Image.open(base_path + image_name)
#     a = np.shape(img_pil)
#     img_pil_r = img_pil.resize((300, 32))
#     b = np.shape(img_pil_r)
#     print(np.shape(img_pil))

# normalize = transforms.Normalize(
#             mean=[0.5070751592371323, 0.48654887331495095, 0.4409178433670343],
#             std=[0.2673342858792401, 0.2564384629170883, 0.27615047132568404]
#         )
#
# preprocess = transforms.Compose([transforms.ToTensor(), normalize])
# path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/pytorch-cifar100/data/test_img/1/img_0914902.jpg'
# # img_pil = Image.open(path)
# # print('*******************', np.shape(img_pil))
# # img_pil = img_pil.resize((32, 256))
# # print('*******************', np.shape(img_pil))
# img_pil = cv2.imread(path)
# print('*******************', np.shape(img_pil))
# img_pil = cv2.resize(img_pil, ((256, 32)))
# print('*******************', np.shape(img_pil))
# img_tensor = preprocess(img_pil)
# print('*******************', np.shape(img_tensor))

# points = [[545, 42], [583, 44], [584, 63], [545, 61]]
# # image = np.zeros((1000, 1000, 3), dtype=np.uint8)
# image = cv2.imread('/Volumes/my_disk/company/sensedeal/dataset/icdar2015/4.1Text Localtion/Training Set/1_ch4_training_images/img_57.jpg')
# image = cv2.polylines(image, np.array([points]), True, (0, 255, 255), 5)
# cv2.imshow('image', image)
# cv2.waitKey()
#
# # # base_path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/data_generator/Generate_det_rec/img/H2_AN202003161376296621_1/'
# image_path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/data_generator/Generate_det_rec/scan/H2_AN202002071374889082_1/'
# label_path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/data_generator/Generate_det_rec/scan/H2_AN202002071374889082_1/'
# image_path = '/Volumes/my_disk/company/sensedeal/dataset/icdar2015/4.1Text Localtion/Training Set/1_ch4_training_images/'
# label_path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/DB_torch_17/datasets/icdar2015/train_gts/'
# image_path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/DB_torch_17/datasets/ocr_det/train_images/'
# label_path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/DB_torch_17/datasets/ocr_det/train_gts/'
# image_path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/exchange/img/'
# label_path = '/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/exchange/img/'
image_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_1/'
label_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_1/'
image_name_list = os.listdir(image_path)
for image_name in image_name_list:
    if image_name.endswith('.txt'):
        continue
    image = cv2.imread(image_path + image_name)
    # lines = open(label_path + image_name.replace('.jpg', '.jpg.txt'), 'r').readlines()
    lines = open(label_path + image_name.replace('.jpg', '.txt'), 'r').readlines()
    for line in lines:
        line = line.lstrip('\ufeff')
        box = line.split(',', 8)[:8]
        content = line.split(',', 8)[-1]
        print(content)
        box = [int(i) for i in box]
        points = np.array([[box[0], box[1]], [box[2], box[3]], [box[4], box[5]], [box[6], box[7]]])
        # box_fintune = 8
        # points = np.array([[box[0]-box_fintune, box[1]-box_fintune], [box[2]+box_fintune, box[3]-box_fintune], [box[4]+box_fintune, box[5]+box_fintune], [box[6]-box_fintune, box[7]+box_fintune]], dtype=np.int)
        image = cv2.polylines(image, np.array([points]), True, (0, 0, 255), 2)
        # image = cv2.polylines(image, np.array([[[45, 272], [215, 273], [212, 296], [45, 290]]]), True, (0, 0, 255), 5)
    cv2.imshow('image', cv2.resize(image, (np.shape(image)[1]//2, np.shape(image)[0]//2)))
    # cv2.imshow('image', cv2.resize(image, (np.shape(image)[1], np.shape(image)[0])))
    cv2.waitKey()

# a = '\u6709\u610f\u8005\u8bf7\u8054\u7cfb'
# print(a)

# print('\ufeff')
# import pdfplumber
#
# pdf = pdfplumber.open('/Volumes/my_disk/company/sensedeal/dataset/pdf/H2_AN201909111355192719_1.pdf')
# page = pdf.pages[0]
# text = page.extract_words()
# print(text)
# print(type(text))

# a = [[14, 5], [52, 8]]
# for i, j in enumerate(a):
#     print(i, j)
# a = 'sadkfjaldk,'
# a.rstrip(',').split('j')
# print(a)
# a = '25+10+10+23.8+25+10+25+25+10+10+10+25+25+9+25+10+10+25+10+9+9.5+24.75+25+22.4+10+24.4+25+9.5+10+25+25+10+24+10+10+25+22.7+22.35+25+25+10+25+23+23+24+24'
# print(len(a.split('+')))
# print(42+4)
#
# print(25+10+10+25+25+10+25+25+10+10+10+25+25+10+25+10+10+25+10+10+10+25+25+22.4+10+25+25+10+10+25+25+10+25+10+10+25+23+22.35+25+25+10+25+23+23+24+24)
# print(25+10+10+23.8+25+10+25+25+10+10+10+25+25+9+25+10+10+25+10+9+9.5+24.75+25+22.4+10+24.4+25+9.5+10+25+25+10+24+10+10+25+22.7+22.35+25+25+10+25+23+23+24+24)
