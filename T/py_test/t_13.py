import numpy as np
import cv2
import chardet


base_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/CRNN_Chinese_Characters_Rec/lib/dataset/txt/char_std.txt'
file = open(base_path, "r", encoding="latin1").readlines()

count = 0
chn_list = []
for line in file:
    count += 1
    line_chn = line.encode('latin1').decode('GB18030').rstrip('\n')
    chn_list.append(line_chn)

lines = open('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_16/train_360_filter.txt', 'r').readlines()
for line in lines:
    image_name = line.split(' ', 1)[0]
    text = line.split(' ', 1)[-1]
    char_list = text.strip('\n').split(' ')
    text = ''
    for char_ in char_list:
        text += chn_list[int(char_)]
    print(text)
    image = cv2.imread('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_16/out_buffer/' + image_name)
    cv2.imshow('image', image)
    cv2.waitKey()
