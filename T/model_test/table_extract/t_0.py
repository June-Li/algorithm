import os
import cv2
import numpy as np
from Functions.line_detection import line_detection


base_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/doc/my_imgs_11/'
image_name_list = os.listdir(base_path)

for image_name in image_name_list:
    image = cv2.imread(base_path + image_name)

    img_h, img_w, _ = np.shape(image)
    if img_h > 1000:
        resize_h = 1000
    else:
        resize_h = img_w

    temp_lines_hor, temp_lines_ver = line_detection(image)
    temp_lines_hor.append([0, 0, img_w, 0])
    temp_lines_hor.append([0, img_h, img_w, img_h])
    temp_lines_ver.append([0, 0, 0, img_h])
    temp_lines_ver.append([img_w, 0, img_w, img_h])

    show_img = image.copy()

    temp = []
    for line in temp_lines_hor:
        x1, y1, x2, y2 = line
        if abs(x1 - x2) / img_w > 0.618:
            temp.append([x1, y1, x2, y2])
    temp_lines_hor = temp
    for i in temp_lines_hor:
        cv2.line(show_img, (i[0], i[1]), (i[2], i[3]), (0, 0, 255), 2)

    temp = []
    for line in temp_lines_ver:
        x1, y1, x2, y2 = line
        if abs(y1 - y2) / img_h > 0.618:
            temp.append([x1, y1, x2, y2])
    temp_lines_ver = temp
    for i in temp_lines_ver:
        cv2.line(show_img, (i[0], i[1]), (i[2], i[3]), (0, 0, 255), 2)
    cv2.imshow('show_img', cv2.resize(show_img, (resize_h * img_w//img_h, resize_h)))
    cv2.waitKey()
