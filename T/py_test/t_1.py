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


def draw_box(image, label):
    for line in label:
        line = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        [x_center, y_center, weight, height] = [float(i) for i in line[1:]]
        x_0 = int((x_center - weight / 2) * np.shape(image)[1])
        y_0 = int((y_center - height / 2) * np.shape(image)[0])
        x_1 = int((x_center + weight / 2) * np.shape(image)[1])
        y_1 = int((y_center + height / 2) * np.shape(image)[0])
        cv2.rectangle(image, (x_0, y_0), (x_1, y_1), (0, 0, 255), thickness=2)
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
    data_path = '/workspace/JuneLi/bbtv/SensedealImgAlg/DATASETS/DET/TableDet/v0/images/train/'

    hostname = "192.168.1.217"
    port = 10022
    username = "root"
    password = "123456"

    sftp, sftp_client = get_remote(hostname, port, username, password)

    image_name_list = sftp.listdir(data_path)

    for index, image_name in enumerate(image_name_list):
        if not image_name.startswith('total_2_44.jpg'):
            continue
        print(image_name)
        image, label = get_image_label(sftp_client, data_path + image_name,
                                       data_path.replace('/images/', '/labels/') + image_name.replace('.jpg', '.txt'))

        image = draw_box(image, label)
        image = cv2.resize(image, (256, 256))
        cv2.imshow('image', image)
        cv2.waitKey()


if __name__ == '__main__':
    main()

