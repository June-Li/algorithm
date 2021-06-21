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

    # label = [line for line in sftp_client.open(label_path)]

    return image, image


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
        for i in line[1:]:
            if float(i) > 1 or float(i) < 0:
                print('oh my god: ', line)
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
    # data_path = '/workspace/JuneLi/bbtv/SSL_yolov3_seal_FixMatch/data/ocr_table/semi/un_images/train/'
    # data_path = '/workspace/JuneLi/bbtv/SSL_yolov3_table_cell_FixMatch/data/ocr_table/all/images/train/'
    # data_path = '/workspace/JuneLi/bbtv/SensedealImgAlg/WORKFLOW/DET/TableDet/v1/test_data/my_imgs_0/'
    data_path = '/workspace/JuneLi/bbtv/SensedealImgAlg/DATASETS/DET/TableDet/v0/images/test_web_download_pad_250/'

    hostname = "192.168.1.217"
    port = 10022
    username = "root"
    password = "123456"

    sftp, sftp_client = get_remote(hostname, port, username, password)

    image_name_list = sftp.listdir(data_path)
    radio_dict = {i: 0 for i in range(10)}
    radio_dict['full'] = 0
    for index, image_name in enumerate(image_name_list):
        # if image_name != 'H2_AN201911291371261448_1_32_0.jpg':
        #     continue
        if image_name == 'coords.txt':
            continue
        print(image_name)
        image, label = get_image_label(sftp_client, data_path + image_name,
                                       data_path.replace('/images/', '/labels_correction/') + image_name.replace('.jpg', '.txt'))

        # radio = get_effective_radio(image, label)
        # radio = 1
        # if not len(label) > 0:
        #     continue
        # if radio < 1:
        #     radio_dict[int(radio*10)] += 1
        # else:
        #     radio_dict['full'] += 1
        #
        # if radio > 0.7:
        #     image = draw_box(image, label)
        #     cv2.imshow('image', image)
        #     cv2.waitKey()
        # if index % 100 == 0:
        #     print(index)
        #     print(radio_dict)

        cv2.imshow('image', image)
        cv2.waitKey()
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
