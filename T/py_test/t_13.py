import cv2
import shutil
import os
import numpy as np


# one_path = '/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/have_seal_unlabel/images/'
# two_path = '/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/have_seal_label/images/test/'
#
# one_image_name_list = os.listdir(one_path)
# two_image_name_list = os.listdir(two_path)
#
# count = 0
# for two_image_name in two_image_name_list:
#     if two_image_name in one_image_name_list:
#         os.remove(one_path + two_image_name)
#         count += 1
# print('total: ', count)


# label_name_list = os.listdir('/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/have_seal_label/labels/test/')
# count = 0
# for label_name in label_name_list:
#     image_name = label_name.replace('.txt', '.jpg')
#     shutil.move('/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/have_seal_unlabel/images/' + image_name,
#                 '/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/have_seal_label/images/test/' + image_name)
#     count += 1
# print('total: ', count)
