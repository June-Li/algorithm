"""
# 用腐蚀膨胀的方法找横线和竖线
import os
import cv2
import numpy as np
from scipy import ndimage

base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_1/'
image_name_list = os.listdir(base_path)

scale = 20
el_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, scale))
el_h = cv2.getStructuringElement(cv2.MORPH_RECT, (scale, 1))

for image_name in image_name_list:
    gray = cv2.imread(base_path + image_name, 0)
    cv2.imshow('gray', gray)

    threshold = cv2.adaptiveThreshold(np.invert(gray), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -2)

    threshold_h = cv2.erode(threshold, el_h)
    threshold_v = cv2.erode(threshold, el_v)

    cv2.imshow('test', threshold_h + threshold_v)
    cv2.waitKey()
"""

"""
# 霍夫找线
image = cv2.imread('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_1/1-8.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# threshold = cv2.adaptiveThreshold(np.invert(gray), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -2)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)  # apertureSize是sobel算子大小，只能为1,3,5，7

lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50,
                        maxLineGap=10)  # 函数将通过步长为1的半径和步长为π/180的角来搜索所有可能的直线
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imshow("line_detect_possible_demo", image)
cv2.waitKey()
"""