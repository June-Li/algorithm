import os
import cv2
import numpy as np

# 显示box，用来检验生成的box是否正确
image_path = '/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/have_seal_label/images/train/'
label_path = '/Volumes/my_disk/company/sensedeal/dataset/公告扫描件/have_seal_label/labels/train/'
image_name_list = os.listdir(image_path)
for image_name in image_name_list:
    # if image_name != '5675_015.jpg':
    #     continue
    print(image_name)
    label_name = image_name.replace('.jpg', '.txt')
    img_path = image_path + image_name
    lab_path = label_path + label_name
    image = cv2.imread(img_path)
    cv2.imshow('ori_image', cv2.resize(image, (np.shape(image)[1] // 2, np.shape(image)[0] // 2)))
    lines = open(lab_path, 'r').readlines()
    for line in lines:
        ii = {0: 'yes', 1: 'no'}
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * np.shape(image)[1])
        y_0 = int((y_center - height / 2) * np.shape(image)[0])
        x_1 = int((x_center + weight / 2) * np.shape(image)[1])
        y_1 = int((y_center + height / 2) * np.shape(image)[0])
        cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (255, 0, 0), thickness=3)
    cv2.imshow('image', cv2.resize(image, (np.shape(image)[1]*1000//np.shape(image)[0], 1000)))
    cv2.waitKey()

