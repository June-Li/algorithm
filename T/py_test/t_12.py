import os
import cv2
import numpy as np

# 显示box，用来检验生成的box是否正确
image_path = '/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/gt/images_dup/'
label_path = '/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/gt/labels_dup/'
# image_path = '/Volumes/my_disk/company/sensedeal/dataset/my/my_mix/table_detection/v_0/TableBank_cls/images/'
# label_path = '/Volumes/my_disk/company/sensedeal/dataset/my/my_mix/table_detection/v_0/TableBank_cls/labels/'
# image_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/SSL_yolov3_FixMatch/data/ocr_table/un_images/train/'
# label_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/SSL_yolov3_FixMatch/data/ocr_table/un_labels/train/'
image_name_list = os.listdir(image_path)
for image_name in image_name_list:
    if not image_name.endswith('.jpg'):
        continue
    print(image_name)
    label_name = image_name.replace('.jpg', '.txt')
    img_path = image_path + image_name
    lab_path = label_path + label_name

    image_ori = cv2.imread(img_path)
    cv2.imshow('ori_image', cv2.resize(image_ori, (np.shape(image_ori)[1] // 2, np.shape(image_ori)[0] // 2)))
    image_gt = cv2.imread(img_path)
    image_all = cv2.imread(img_path)
    lines = open(lab_path, 'r').readlines()
    si_flag = True
    tran_img = ''
    for line in lines:
        ii = {0: 'yes', 1: 'no'}
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * np.shape(image_gt)[1])
        y_0 = int((y_center - height / 2) * np.shape(image_gt)[0])
        x_1 = int((x_center + weight / 2) * np.shape(image_gt)[1])
        y_1 = int((y_center + height / 2) * np.shape(image_gt)[0])
        cv2.rectangle(image_gt, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=1)
        cv2.rectangle(image_all, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=1)

        if si_flag:
            ss = image_ori.copy()
            cv2.rectangle(ss, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=3)
            cv2.imshow('ss', ss)
            key = cv2.waitKey()
            if key == ord(' '):
                tran_img = ss
                si_flag = False
    cv2.imwrite('/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/gt/out/gt.jpg', image_gt)

    image_p = cv2.imread(img_path)
    lines = open(lab_path.replace('labels_dup', 'labels_p'), 'r').readlines()
    for line in lines:
        ii = {0: 'yes', 1: 'no'}
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * np.shape(image_p)[1])
        y_0 = int((y_center - height / 2) * np.shape(image_p)[0])
        x_1 = int((x_center + weight / 2) * np.shape(image_p)[1])
        y_1 = int((y_center + height / 2) * np.shape(image_p)[0])
        cv2.rectangle(image_p, (x_0, y_0), (x_1, y_1), (255, 0, 0), thickness=1)
        cv2.rectangle(image_all, (x_0, y_0), (x_1, y_1), (255, 0, 0), thickness=1)


        ss = tran_img.copy()
        cv2.rectangle(ss, (x_0, y_0), (x_1, y_1), (255, 0, 0), thickness=3)
        cv2.imshow('ss', ss)
        key = cv2.waitKey()
    cv2.imwrite('/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/gt/out/predict.jpg', image_p)

    cv2.putText(image_all, 'single table mAP: ' + str(0.833), (100, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(125, 125, 255), fontScale=2, thickness=3)
    cv2.imwrite('/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/gt/out/gt+predict.jpg', image_all)
    cv2.imshow('image', cv2.resize(image_gt, (np.shape(image_gt)[1] * 1000 // np.shape(image_gt)[0], 1000)))
    cv2.imshow('image', cv2.resize(image_p, (np.shape(image_p)[1]*1000//np.shape(image_p)[0], 1000)))
    cv2.imshow('image', cv2.resize(image_all, (np.shape(image_p)[1] * 1000 // np.shape(image_p)[0], 1000)))
    cv2.waitKey()

