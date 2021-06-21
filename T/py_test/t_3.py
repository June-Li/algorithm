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


def main():
    data_path = '/workspace/JuneLi/datasets/paddleocr推荐的中文训练数据集/ICDAR2019-ArT/train_images/'
    data_path = '/root/bbtv/pytorch-cifar100/data/ocr_angle/out/1/'
    data_path = '/workspace/JuneLi/bbtv/PytorchOCR/out/my_imgs_2/3/'

    hostname = "192.168.1.217"
    port = 10022
    username = "root"
    password = "123456"

    sftp, sftp_client = get_remote(hostname, port, username, password)

    image_name_list = sftp.listdir(data_path)
    radio_dict = {i: 0 for i in range(10)}
    radio_dict['full'] = 0
    for index, image_name in enumerate(image_name_list):
        # if image_name != 'gt_1924.jpg':
        #     continue
        print(image_name)
        image, label = get_image_label(sftp_client, data_path + image_name,
                                       data_path.replace('/images/', '/labels/') + image_name.replace('.jpg', '.txt'))

        # print('label is: ', label)
        cv2.imshow('image', image)
        cv2.waitKey()


if __name__ == '__main__':
    main()
