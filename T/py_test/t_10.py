import numpy as np
import os
import sys
import cv2
import shutil


base_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/crawl/百度-发票盖章/'
out_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/crawl_filter/baidu_fapiao_images/'
image_name_list = os.listdir(base_path)
for index, image_name in enumerate(image_name_list):
    if os.path.exists(out_path + image_name):
        continue
    try:
        print(image_name)
        image = cv2.imread(base_path + image_name)
        cv2.imshow('image', image)
        key = cv2.waitKey()
        if key == ord(' '):
            shutil.copy(base_path + image_name, out_path + image_name)
    except:
        print(image_name)
    print('processed num: ', index)
