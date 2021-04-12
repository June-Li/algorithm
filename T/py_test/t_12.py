import numpy as np
import cv2
import chardet

#
# file = open('', 'r')
# lines = file.readlines()
# for line in lines:
#     print(line)

"""
num_125304.jpg 76 6 6 105 105 19
pdf_scan_H2_AN202003311377255325_1_39_159.jpg 22 6 19 94 26
global_425583.jpg 205
54779468_1432822555.jpg 2 92 39 175 75 58 477 4 543 14
global_884609.jpg 76 6 19 105 19 105
"""

base_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/CRNN_Chinese_Characters_Rec/lib/dataset/txt/char_std_5990.txt'
file = open(base_path, "r", encoding="latin1").readlines()

count = 0
chn_list = []
for line in file:
    count += 1
    line_chn = line.encode('latin1').decode('GB18030').rstrip('\n')
    chn_list.append(line_chn)
# # # print(chn_list.index('：'))
# print(chn_list.index('１'))
print(chn_list.index('1'))
print(chardet.detect(str.encode('１')))
print(chardet.detect(str.encode('1')))
print(chardet.detect(str.encode('：')))
print(chardet.detect(str.encode(chn_list[49])), chn_list[49])
print(ord('1'), ord('１'), '１'.encode('utf8'))

char_list = '223 382 376 403 20 226 98 20'.split(' ')
text = ''
for char_ in char_list:
    text += chn_list[int(char_)]
print(text)

# a = '123548dsafsdfa我的'
# # a = 'lijun李俊+'
# num_count = 0
# for char in list(a):
#     if char in list('012345789'):
#         num_count += 1
# print(num_count)
# if num_count > 5:
#     print(a)

# base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_15/global_999895.jpg'
# while True:
#     image = cv2.imread(base_path)
#     image = cv2.resize(image, (32 * np.shape(image)[1] // np.shape(image)[0], 32))
#     if np.shape(image)[1] >= 280:
#         image = cv2.resize(image, (280, 32))
#     else:
#         mask_image = np.ones((32, 280, 3), dtype=np.uint8) * int(np.argmax(np.bincount(image.flatten(order='C'))))
#         random_index = np.random.randint(0, 280 - np.shape(image)[1])
#         mask_image[:, random_index: random_index + np.shape(image)[1]] = image
#         image = mask_image
#     cv2.imshow('image', image)
#     cv2.waitKey(1)
