import os
import cv2
import numpy as np


def cal_iou(box_1, box_2):
    iou, overlap_area = 0, 0
    min_x = min(box_1[0], box_1[2], box_2[0], box_2[2])
    max_x = max(box_1[0], box_1[2], box_2[0], box_2[2])
    min_y = min(box_1[1], box_1[3], box_2[1], box_2[3])
    max_y = max(box_1[1], box_1[3], box_2[1], box_2[3])
    box_1_w = abs(box_1[0] - box_1[2])
    box_1_h = abs(box_1[1] - box_1[3])
    box_2_w = abs(box_2[0] - box_2[2])
    box_2_h = abs(box_2[1] - box_2[3])
    merge_w = max_x - min_x
    merge_h = max_y - min_y
    overlap_w = box_1_w + box_2_w - merge_w
    overlap_h = box_1_h + box_2_h - merge_h
    if overlap_h > 0 and overlap_w > 0:
        box_1_area = box_1_w * box_1_h
        box_2_area = box_2_w * box_2_h
        overlap_area = overlap_w * overlap_h
        iou = overlap_area / (box_1_area + box_2_area - overlap_area)
    return iou


predict_base_path = '/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/gt/'
predict_image_path = predict_base_path + 'images_p/'
predict_label_path = predict_base_path + 'labels_p/'

gt_base_path = '/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/gt/'
gt_image_path = gt_base_path + 'images_dup/'
gt_label_path = gt_base_path + 'labels_dup/'

predict_iou_list_iou_list_total = []
gt_iou_list_iou_list_total = []
label_name_list = os.listdir(predict_label_path)
for label_name in label_name_list:
    image = cv2.imread(gt_image_path + label_name.replace('.txt', '.jpg'))
    h, w, _ = np.shape(image)
    resize_max = 1300
    resize_h, resize_w = h, w
    if h > w:
        if h > resize_max:
            resize_h, resize_w = resize_max, resize_max * w // h
    else:
        if w > resize_max:
            resize_h, resize_w = resize_max * h // w, resize_max

    predict_image = image.copy()
    predict_lines = open(predict_label_path + label_name, 'r')
    predict_boxes = []
    for line in predict_lines:
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * np.shape(image)[1])
        y_0 = int((y_center - height / 2) * np.shape(image)[0])
        x_1 = int((x_center + weight / 2) * np.shape(image)[1])
        y_1 = int((y_center + height / 2) * np.shape(image)[0])
        predict_boxes.append([x_0, y_0, x_1, y_1])
    #     cv2.rectangle(predict_image, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=2)
    # cv2.imshow('predict_image', cv2.resize(predict_image, (resize_w, resize_h)))

    gt_image = image.copy()
    gt_lines = open(gt_label_path + label_name, 'r')
    gt_boxes = []
    for line in gt_lines:
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * np.shape(image)[1])
        y_0 = int((y_center - height / 2) * np.shape(image)[0])
        x_1 = int((x_center + weight / 2) * np.shape(image)[1])
        y_1 = int((y_center + height / 2) * np.shape(image)[0])
        gt_boxes.append([x_0, y_0, x_1, y_1])
    #     cv2.rectangle(gt_image, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=2)
    # cv2.imshow('gt_image', cv2.resize(gt_image, (resize_w, resize_h)))
    # cv2.waitKey()

    # 以predict算gt
    predict_iou_list = []
    for gt_box in gt_boxes:
        max_iou = -999
        for predict_box in predict_boxes:
            iou = cal_iou(gt_box, predict_box)
            if iou > max_iou:
                max_iou = iou
        if max_iou > 0:
            predict_iou_list.append(max_iou)
        else:
            predict_iou_list.append(0)

    # 以gt算predict
    gt_iou_list = []
    for predict_box in predict_boxes:
        max_iou = -999
        for gt_box in gt_boxes:
            iou = cal_iou(gt_box, predict_box)
            if iou > max_iou:
                max_iou = iou
        if max_iou > 0:
            gt_iou_list.append(max_iou)
        else:
            gt_iou_list.append(0)

    predict_iou_list_iou_list_total.append(np.average(predict_iou_list))
    gt_iou_list_iou_list_total.append(np.average(gt_iou_list))
    print()
print('predict_iou_list_iou_list_total: ', np.average(predict_iou_list_iou_list_total))
print('gt_iou_list_iou_list_total: ', np.average(gt_iou_list_iou_list_total))
