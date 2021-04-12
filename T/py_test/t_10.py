# import os
# import cv2
# import numpy as np
# import time
#
# # 显示box，用来检验生成的box是否正确
# image_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/buffer/DB_train/datasets/ocr_det/train_images/'
# label_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/buffer/DB_train/datasets/ocr_det/train_gts/'
# image_name_list = os.listdir(image_path)
# for image_name in image_name_list:
#     if image_name.endswith('.txt'):
#         continue
#     image = cv2.imread(image_path + image_name, 0)
#     lines = open(label_path + image_name.replace('.jpg', '.jpg.txt'), 'r').readlines()
#     for line in lines:
#         box = line.split(',')[:-2]
#         box = [int(i) for i in box]
#         points = np.array([[box[0], box[1]], [box[2], box[3]], [box[4], box[5]], [box[6], box[7]]])
#         image = cv2.polylines(image, np.array([points]), True, (0, 255, 255), 5)
#         s_time = time.time()
#         image = cv2.fillPoly(image, np.array([points]), 1)
#         print('use time: ', time.time()-s_time)
#     cv2.imshow('image', cv2.resize(image, (np.shape(image)[1]//2, np.shape(image)[0]//2)))
#     cv2.waitKey()


import os
import cv2
import numpy as np

# 显示box，用来检验生成的box是否正确
# image_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_14/test/img/H2_AN202004211378311212_1/'
# label_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_14/test/img/H2_AN202004211378311212_1/'
# image_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_14/H2_AN201911181370834963_1/'
# label_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_14/H2_AN201911181370834963_1/'
image_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_14/test_3/images/'
label_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_14/test_3/labels/'
image_name_list = os.listdir(image_path)
for image_name in image_name_list:
    if image_name.endswith('.txt'):
        continue
    print(image_name)
    label_name = image_name.replace('.jpg', '.txt')
    img_path = image_path + image_name
    lab_path = label_path + label_name
    image = cv2.imread(img_path)
    lines = open(lab_path, 'r').readlines()
    for line in lines:
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * np.shape(image)[1])
        y_0 = int((y_center - height / 2) * np.shape(image)[0])
        x_1 = int((x_center + weight / 2) * np.shape(image)[1])
        y_1 = int((y_center + height / 2) * np.shape(image)[0])
        cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=2)
    cv2.imshow('image', cv2.resize(image, (np.shape(image)[1] // 2, np.shape(image)[0] // 2)))
    cv2.waitKey()
