# import cv2
# import numpy as np
# import os
# import shutil
#
# # base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/20210423评估/'
# # tencent_out_path = base_path + 'tencent_out/images/'
# # gt_image_path = base_path + 'my_out/images/'
# # for i in range(15):
# #     print(i)
# #     image_1 = cv2.imread(tencent_out_path + str(i) + '.jpg')
# #     image_2 = cv2.imread(gt_image_path + str(i) + '.jpg')
# #     print(np.shape(image_1))
# #     print(np.shape(image_2))
# #     cv2.imshow('image_1', image_1)
# #     cv2.imshow('image_2', image_2)
# #     cv2.waitKey()
#
#
#
# # base_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/result/my_imgs_gt_0/'
# # out_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_18/20210423评估/my_out/images/'
# # image_name_list = os.listdir(base_path)
# # for image_name in image_name_list:
# #     # shutil.copy(base_path + image_name + '/' + image_name + '_0_table_ori_0.jpg', out_path + image_name + '_0_table_ori_0.jpg')
# #     # shutil.copy(base_path + image_name + '/' + image_name + '_0_table_ori_0_yolo_box.txt', out_path.replace('/images/', '/labels/') + image_name + '_0_table_ori_0_yolo_box.txt')
# #     shutil.copy(base_path + image_name + '/' + image_name + '_0_table_draw_0.jpg', out_path.replace('/images/', '/show/') + image_name + '_0_table_draw_0.jpg')
# #     shutil.copy(base_path + image_name + '/' + image_name + '.txt', out_path.replace('/images/', '/struct/') + image_name + '.txt')
# #     shutil.copy(base_path + image_name + '/' + image_name + '_0_table_structure_0.html', out_path.replace('/images/', '/struct/') + image_name + '_0_table_structure_0.html')
#
#
# import base64
# f_ = open('/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/doc/biaozhupingtai_20210427/liushui/浦发银行对公流水.jpeg', 'rb')
# img_ = base64.b64encode(f_.read())
# f = open('/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/doc/biaozhupingtai_20210427/liushui/浦发银行对公流水.jpeg', 'rb')
# img = base64.b64encode(f.read()).decode('utf8')
# print(img)

# a = [1, 1, 1, 1, 1]
# b = [1, 1, 1, 0, 0]
# print(a*b)


import cv2
import numpy as np

image = cv2.imread('/Volumes/my_disk/company/sensedeal/PycharmProject/bbtv/PytorchOCR/doc/my_imgs/imgs_0/2.jpg')
out_img = np.concatenate((image, image), axis=1)
cv2.imshow('image', out_img)
cv2.waitKey()
