import os
import cv2
import numpy as np

# 显示box，用来检验生成的box是否正确
# image_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_17/show_cell/H2_AN202001171374309841_1/'
# label_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_17/show_cell/H2_AN202001171374309841_1/'
# image_path = '/Volumes/my_disk/company/sensedeal/dataset/my/my_mix/table_detection/v_0/TableBank_cls/images/'
# label_path = '/Volumes/my_disk/company/sensedeal/dataset/my/my_mix/table_detection/v_0/TableBank_cls/labels/'
image_path = '/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/gt/images/'
label_path = '/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/gt/labels/'
image_name_list = os.listdir(image_path)
for image_name in image_name_list:
    # if image_name != '5675_015.jpg':
    #     continue
    if image_name.endswith('.txt'):
        continue
    # if image_name != 'H2_AN202004211378311212_1_6_0_noline.jpg':
    #     continue
    print(image_name)
    label_name = image_name.replace('.jpg', '.txt')
    img_path = image_path + image_name
    lab_path = label_path + label_name
    image = cv2.imread(img_path)
    cv2.imshow('ori_image', cv2.resize(image, (np.shape(image)[1] // 2, np.shape(image)[0] // 2)))
    lines = open(lab_path, 'r').readlines()
    # out_file = open('/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/DB_train/datasets/ocr_det/train_gts/H2_AN202004211378311212_1_6_0_noline.txt', 'a+')
    for line in lines:
        ii = {0: 'yes', 1: 'no'}
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * np.shape(image)[1])
        y_0 = int((y_center - height / 2) * np.shape(image)[0])
        x_1 = int((x_center + weight / 2) * np.shape(image)[1])
        y_1 = int((y_center + height / 2) * np.shape(image)[0])
        cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=2)
        # cv2.putText(image, ii[int(line[0])], (x_0, y_0), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 255, 0), 12)
        # out_file.write(str(x_0) + ',' + str(y_0) + ',' +
        #                str(x_1) + ',' + str(y_0) + ',' +
        #                str(x_1) + ',' + str(y_1) + ',' +
        #                str(x_0) + ',' + str(y_1) + ',' +
        #                '###' + ',\n')
    # cv2.namedWindow('image', 0)
    cv2.imshow('image', cv2.resize(image, (np.shape(image)[1]*1000//np.shape(image)[0], 1000)))
    cv2.waitKey()

