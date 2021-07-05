# # class dataloader:
# #     def __init__(self):
# #         pass
# #
# #     def __len__(self):
# #         pass
# #
# #     def __getitem__(self, item):
# #         return item
# #
# #
# # data = dataloader()
# # for i in range(99):
# #     print(data[i])
#
# # import numpy as np
# #
# # rotated_points = np.array([[1, 10], [2, 2], [3, 3], [4, 4]])
# # rotated_points_sum = np.sum(rotated_points, axis=-1)
# # print(rotated_points_sum)
# # x_min_index = np.argmin(rotated_points_sum)
# # print(x_min_index)
#
# import cv2
# import numpy as np
# import os
#
# base_path = '/Volumes/my_disk/company/sensedeal/temp/'
# image_path = base_path + '/table/images/'
# label_path = base_path + '/table/labels/'
# image_name_list = os.listdir(image_path)
# expand = 500
# for image_name in image_name_list:
#     # if image_name != '29.jpg':
#     #     continue
#     image = cv2.imread(image_path + image_name)
#     line = open(label_path + image_name.replace('.jpg', '.txt'), 'r').readline()
#     line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
#     [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
#     x_0 = int((x_center - weight / 2) * np.shape(image)[1])
#     y_0 = int((y_center - height / 2) * np.shape(image)[0])
#     x_1 = int((x_center + weight / 2) * np.shape(image)[1])
#     y_1 = int((y_center + height / 2) * np.shape(image)[0])
#
#     bg_value = int(np.argmax(np.bincount(image.flatten(order='C'))))
#     ori_h, ori_w = np.shape(image)[0], np.shape(image)[1]
#     expand_image = np.ones((ori_h + expand, ori_w + expand, 3), dtype=np.uint8) * bg_value
#     expand_image[expand//2:expand//2 + ori_h, expand//2:expand//2 + ori_w] = image
#     image = expand_image
#
#     x_0 += expand//2
#     y_0 += expand//2
#     x_1 += expand//2
#     y_1 += expand//2
#
#     x_center = (abs(x_0+x_1)/2)/(ori_w+expand)
#     y_center = (abs(y_0+y_1)/2)/(ori_h+expand)
#     weight = abs(x_0-x_1)/(ori_w+expand)
#     height = abs(y_0-y_1)/(ori_h+expand)
#
#     out_str = '0 ' + ' '.join([str(x_center), str(y_center), str(weight), str(height)]) + '\n'
#     open(base_path + '/table/labels_pad_250/' + image_name.replace('.jpg', '.txt'), 'a+').writelines(out_str)
#
#
#     # out_image = image[y_0:y_1, x_0:x_1]
#     cv2.imwrite(base_path + '/table/images_pad_250/' + image_name, image)
#     # cv2.imshow('out_image', image)
#     # cv2.waitKey()
#     # cv2.imshow('image', image)
#     # cv2.waitKey()
#
# # import os
# #
# #
# # base_path = '/Volumes/my_disk/company/sensedeal/temp/table_cell/line/labels/'
# # name_list = os.listdir(base_path)
# # count = 0
# # for name in name_list:
# #     lines = open(base_path + name, 'r').readline()
# #     print(len(lines))
# #     count += len(lines)
# # print(count)
# # import numpy as np
# # rot_flag_list_ = [True, True, True, False, False]
# # rot_flag_list_bitcount_index = np.argmax(np.bincount(rot_flag_list_))
# # print(rot_flag_list_bitcount_index)
# # print(np.bincount(rot_flag_list_))
#
# # import math
# # import numpy as np
# #
# # box_list = [
# #     [
# #         [0, 0],
# #         [100, 100],
# #         [100, 110],
# #         [0, 10]
# #     ],
# #     [
# #         [0, 0],
# #         [100, 100],
# #         [100, 110],
# #         [0, 10]
# #     ],
# #     [
# #         [0, 0],
# #         [100, 100],
# #         [100, 110],
# #         [0, 10]
# #     ],
# #     [
# #         [90, 0],
# #         [100, 0],
# #         [0, 90],
# #         [0, 100]
# #     ],
# # ]
# # tilt_angle_list = []
# # for box in box_list:
# #     point_0 = box[0]
# #     point_1 = box[1]
# #     point_2 = box[2]
# #     point_3 = box[3]
# #     h = abs(point_1[1] - point_2[1])
# #     w = abs(point_0[0] - point_1[0])
# #     if w / h < 2.5 and h / w < 2.5:
# #         continue
# #
# #     if w > h:
# #         p_0 = [(point_0[0] + point_3[0]) // 2, (point_0[1] + point_3[1]) // 2]
# #         p_1 = [(point_1[0] + point_2[0]) // 2, (point_1[1] + point_2[1]) // 2]
# #     else:
# #         p_0 = [(point_0[0] + point_1[0]) // 2, (point_0[1] + point_1[1]) // 2]
# #         p_1 = [(point_2[0] + point_3[0]) // 2, (point_2[1] + point_3[1]) // 2]
# #
# #     if (p_0[0] - p_1[0]) * (p_0[1] - p_1[1]) > 0:
# #         tilt_angle_list.append(
# #             90 + int(round(math.degrees(math.atan((abs(p_0[0] - p_1[0])) / (abs(p_0[1] - p_1[1]) + 0.000001))), 0)))
# #     else:
# #         tilt_angle_list.append(
# #             int(round(math.degrees(math.atan((abs(p_0[1] - p_1[1])) / (abs(p_0[0] - p_1[0]) + 0.000001))), 0)))
# # print(tilt_angle_list)
# # tilt_angle_list_bitcount_index = np.argmax(np.bincount(tilt_angle_list))
# # print(np.bincount(tilt_angle_list))
# # print(tilt_angle_list_bitcount_index)

import numpy as np
import math
import cv2

# a = np.array([[[100], [100]], [[210], [100]]])
# # b = np.concatenate((a, a+10), axis=-1)
# b = np.vsplit(a)
# print(b)
# print(math.degrees(math.atan(4/1030)))

# mask_ii = np.zeros((2500, 2500, 3), dtype=np.uint8)
# cv2.polylines(mask_ii, np.array([[[300, 300], [500, 300], [500, 330], [300, 330]]]), True, (255, 255, 255), 2)
# cv2.imshow('ii', mask_ii)
# cv2.waitKey()
a = [
    [[1, 2], [3, 4]],
    [[10, 20], [30, 40]]
]

print(a[:, 0])
