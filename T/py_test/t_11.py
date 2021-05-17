import cv2
import shutil
import os


# base_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/crawl/百度-章程盖章/'
# image_name_list = os.listdir(base_path)
# for image_name in image_name_list:
#     print(image_name)
#     os.rename(base_path + image_name, base_path + 'baidu_zhangcheng_' + image_name)


# base_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/crawl_filter/sougou_fapiao_images/'
# out_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/crawl_all/images/'
# image_name_list = os.listdir(base_path)
# for image_name in image_name_list:
#     shutil.copy(base_path + image_name, out_path + image_name)


# base_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/step_2_crawl_filter/baidu_fapiao_images/'
# out_label_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/step_4_crawl_semi/images/'
# out_unlabel_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/step_4_crawl_semi/un_images/'
# image_name_list = os.listdir(base_path)
# for index, image_name in enumerate(image_name_list):
#     if index % 40 == 0:
#         shutil.copy(base_path + image_name, out_label_path + image_name)
#     else:
#         shutil.copy(base_path + image_name, out_unlabel_path + image_name)
#     print(image_name)
#
# label_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/step_4_crawl_semi/labels-/'
# out_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/step_4_crawl_semi/labels/'
# file_name_list = os.listdir(label_path)
# for file_name in file_name_list:
#     if 'class' in file_name:
#         continue
#     lines = open(label_path + file_name, 'r').readlines()
#     out_str = ''
#     for line in lines:
#         out_str += ' '.join(['0'] + line.split(' ')[1:])
#     open(out_path + file_name, 'w').writelines(out_str)
#     print(out_str)

# base_path = '/Volumes/my_disk/company/sensedeal/dataset/印章/step_4_crawl_semi/'
# in_path = base_path + 'un_images/train/'
# out_path = base_path + 'images/test/'
# image_name_list = os.listdir(in_path)
# num = 0
# for index, image_name in enumerate(image_name_list):
#     if index % 15 == 1:
#         shutil.move(in_path + image_name, out_path + image_name)
#         num += 1
#     if num == 41:
#         break
#     print(image_name)



# -*- coding: utf-8 -*-
# !/usr/bin/env python
import paramiko
import cv2
import numpy as np
import copy


def get_remote(hostname, port, username, password):
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password, compress=True)
    sftp_client = client.open_sftp()
    return sftp, sftp_client


def get_image_label(sftp_client, image_path, label_path):
    image_bin = sftp_client.open(image_path)  # 文件路径
    image = np.asarray(bytearray(image_bin.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    label = [line for line in sftp_client.open(label_path)]

    return image, label


def get_image(sftp_client, image_path):
    image_bin = sftp_client.open(image_path)  # 文件路径
    image = np.asarray(bytearray(image_bin.read()), dtype="uint8")
    image_1 = cv2.imdecode(image, cv2.IMREAD_COLOR)

    image_bin = sftp_client.open(image_path.replace('exp4', 'exp5'))  # 文件路径
    image = np.asarray(bytearray(image_bin.read()), dtype="uint8")
    image_2 = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image_1, image_2


def draw_box(image, label):
    for line in label:
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * np.shape(image)[1])
        y_0 = int((y_center - height / 2) * np.shape(image)[0])
        x_1 = int((x_center + weight / 2) * np.shape(image)[1])
        y_1 = int((y_center + height / 2) * np.shape(image)[0])
        cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 255, 255), thickness=2)
    return image


def get_effective_radio(image, label):
    img_h, img_w, _ = np.shape(image)
    effective_area_list = []
    for line in label:
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * img_w)
        y_0 = int((y_center - height / 2) * img_h)
        x_1 = int((x_center + weight / 2) * img_w)
        y_1 = int((y_center + height / 2) * img_h)
        effective_area_list.append(abs(x_1 - x_0) * abs(y_0 - y_1))
    effective_area = sum(effective_area_list)
    total_area = img_h * img_w
    radio = effective_area / total_area
    return radio


def main():
    data_path = '/workspace/JuneLi/bbtv/SSL_yolov3_seal_FixMatch/runs/detect/exp4/'
    # data_path = '/workspace/JuneLi/bbtv/SSL_yolov3_table_cell_FixMatch/data/ocr_table/all/images/train/'

    hostname = "192.168.1.217"
    port = 10022
    username = "root"
    password = "123456"

    sftp, sftp_client = get_remote(hostname, port, username, password)

    image_name_list = sftp.listdir(data_path)
    radio_dict = {i: 0 for i in range(10)}
    radio_dict['full'] = 0
    for index, image_name in enumerate(image_name_list):
        print(image_name)
        image_1, image_2 = get_image(sftp_client, data_path + image_name)

        cv2.imshow('image_1', image_1)
        cv2.imshow('image_2', image_2)
        key = cv2.waitKey()
        if key == ord(' '):
            cv2.imwrite('out/' + str(index) + '.jpg', image_2)
        if index % 100 == 0:
            print(index)
            print(radio_dict)
    print(radio_dict)


if __name__ == '__main__':
    main()
# data_path = '/workspace/JuneLi/bbtv/SSL_yolov3_table_cell_FixMatch/data/ocr_table/semi/un_images/train/'
# # 实例化一个transport对象
# transport = paramiko.Transport(('192.168.1.217', 10022))
# # 建立连接
# transport.connect(username='root', password='123456')
# # 实例化一个 sftp对象,指定连接的通道
# sftp = paramiko.SFTPClient.from_transport(transport)
# data = sftp.listdir(data_path)
# print(data)
# for imagename in data:
#     imagepath = os.path.join('http://192.168.1.217:10022 ' + data_path, imagename)
#     print(imagepath)
#     resp = urllib.request.urlopen(imagepath)
#     image = np.asarray(bytearray(resp.read()), dtype="uint8")
#     image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#     cv2.imshow('image', image)
#     cv2.waitKey(0)
#     print(image)
# x_list, y_list = [], []
# x_list.append(x_0), x_list.append(x_1), y_list.append(y_0), y_list.append(y_1)
# min_x, min_y, max_x, max_y = min(x_list), min(y_list), max(x_list), max(y_list)
# total_area = abs(max_x - min_x) * abs(max_y * min_y)
