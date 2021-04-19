# import random

# a = [11, 25]
# for i in range(99):
#     b = random.randint(0, len(a))
#     print(b)

# for i in range(100):
#     a = random.randint(0, 100)
#     print(a)

import cv2
import os
import numpy as np

image = cv2.imread('/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/SSL_yolov3_FixMatch/buffer/a.jpg')
# line = '0 0.5 0.28359 0.5011 0.20781'
line = '[          0      47.601      89.157      379.14      177.34]'
line = line.strip('[').strip(']').split(' ')
line = [i for i in line if i != '']
# line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
# [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
# x_0 = int((x_center - weight / 2) * np.shape(image)[1])
# y_0 = int((y_center - height / 2) * np.shape(image)[0])
# x_1 = int((x_center + weight / 2) * np.shape(image)[1])
# y_1 = int((y_center + height / 2) * np.shape(image)[0])
# cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=2)
# cv2.imshow('image', image)
# cv2.waitKey()

[x_0, y_0, x_1, y_1] = [int(float(i)) for i in line[1:]]
cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=2)
cv2.imshow('image', image)
cv2.waitKey()