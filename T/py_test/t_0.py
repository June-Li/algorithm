# # import cv2
# # import numpy as np
# # import random
# #
# # # # 首先读入img
# # # img = cv2.imread('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_19/liv.png', cv2.IMREAD_COLOR)
# # # img = cv2.resize(img, (180, 32))
# # # # N对基准控制点
# # # N = 5
# # # points = []
# # # dx = int(180 / (N - 1))
# # # for i in range(2 * N):
# # #     points.append((dx * i, 4))
# # #     points.append((dx * i, 36))
# # # # 周围拓宽一圈
# # # img = cv2.copyMakeBorder(img, 4, 4, 0, 0, cv2.BORDER_REPLICATE)
# # # # 画上绿色的圆圈
# # # for point in points:
# # #     cv2.circle(img, point, 1, (0, 255, 0), 2)
# # # tps = cv2.createThinPlateSplineShapeTransformer()
# # #
# # # sourceshape = np.array(points, np.int32)
# # # sourceshape = sourceshape.reshape(1, -1, 2)
# # # matches = []
# # # for i in range(1, N + 1):
# # #     matches.append(cv2.DMatch(i, i, 0))
# # #
# # # # 开始随机变动
# # # newpoints = []
# # # PADDINGSIZ = 10
# # # for i in range(N):
# # #     nx = points[i][0] + random.randint(0, PADDINGSIZ) - PADDINGSIZ / 2
# # #     ny = points[i][1] + random.randint(0, PADDINGSIZ) - PADDINGSIZ / 2
# # #     newpoints.append((nx, ny))
# # # print(points, newpoints)
# # # targetshape = np.array(newpoints, np.int32)
# # # targetshape = targetshape.reshape(1, -1, 2)
# # # tps.estimateTransformation(sourceshape, targetshape, matches)
# # # img = tps.warpImage(img)
# # # cv2.imwrite('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_19/tmp.png', img)
# #
# # def minDistance_guanfang(word1, word2):
# #     n = len(word1)
# #     m = len(word2)
# #
# #     # 有一个字符串为空串
# #     if n * m == 0:
# #         return n + m
# #
# #     # DP 数组
# #     D = [[0] * (m + 1) for _ in range(n + 1)]
# #
# #     # 边界状态初始化
# #     for i in range(n + 1):
# #         D[i][0] = i
# #     for j in range(m + 1):
# #         D[0][j] = j
# #
# #     # 计算所有 DP 值
# #     for i in range(1, n + 1):
# #         for j in range(1, m + 1):
# #             left = D[i - 1][j] + 1
# #             down = D[i][j - 1] + 1
# #             left_down = D[i - 1][j - 1]
# #             if word1[i - 1] != word2[j - 1]:
# #                 left_down += 1
# #             D[i][j] = min(left, down, left_down)
# #
# #     return D[n][m]
# #
# #
# # def minDistance_my(word1, word2):
# #     if len(word2) == 0:
# #         return len(word1)
# #     if len(word1) == 0:
# #         return len(word2)
# #
# #     dp = [[0 for _ in range(len(word2))] for _ in range(len(word1))]
# #     for i in range(len(word1)):
# #         for j in range(len(word2)):
# #             if word1[i] == word2[j]:
# #                 if i == 0 and j == 0:
# #                     dp[i][j] = 0
# #                 elif i == 0 and j != 0:
# #                     dp[i][j] = dp[i][j-1]
# #                 elif j == 0 and i != 0:
# #                     dp[i][j] = dp[i-1][j]
# #                 else:
# #                     dp[i][j] = dp[i - 1][j - 1]
# #             else:
# #                 if i == 0 and j == 0:
# #                     dp[i][j] = 1
# #                 elif i == 0 and j != 0:
# #                     dp[i][j] = 1 + dp[i][j - 1]
# #                 elif j == 0 and i != 0:
# #                     dp[i][j] = 1 + dp[i - 1][j]
# #                 else:
# #                     dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])
# #     # dp = [[0 for _ in range(len(word2)+1)] for _ in range(len(word1)+1)]
# #     # for i in range(len(dp[0])):
# #     #     dp[0][i] = i
# #     # for i in range(len(dp)):
# #     #     dp[i][0] = i
# #     # for i in range(1, len(word1)+1):
# #     #     for j in range(1, len(word2)+1):
# #     #         if word1[i-1] == word2[j-1]:
# #     #             dp[i][j] = dp[i - 1][j - 1]
# #     #         else:
# #     #             dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])
# #     return dp[-1][-1]
# #
# #
# # # word1 = "horse"
# # # # word1 = "rosl"
# # # word2 = "ros"
# # # word1 = "intention"
# # # word2 = "execution"
# # # word1 = 'sea'
# # # word2 = 'eat'
# # word1 = "pneumonoultramicroscopicsilicovolcanoconiosis"
# # word2 = "ultramicroscopically"
# # num = minDistance_my(word1, word2)
# # # num = minDistance_guanfang(word1, word2)
# # print(num)
# #
#
#
# import os
# import cv2
# import numpy as np
#
#
# # image_ori = cv2.imread('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_1/have_seal/21.jpg')
# # ori_h, ori_w, _ = np.shape(image_ori)
# #
# # B = image_ori[:, :, 0]
# # G = image_ori[:, :, 1]
# # R = image_ori[:, :, 2]
# #
# # stage = 10
# # B_stage = B//stage
# # G_stage = G//stage
# # R_stage = R//stage
# #
# # B_value = int(np.argmax(np.bincount(B_stage.copy().flatten(order='C'))))
# # G_value = int(np.argmax(np.bincount(G_stage.copy().flatten(order='C'))))
# # R_value = int(np.argmax(np.bincount(R_stage.copy().flatten(order='C'))))
# #
# # mask_img = np.concatenate(
# #     (
# #         np.ones((ori_h, ori_w, 1), dtype=np.uint8)*B_value*stage,
# #         np.ones((ori_h, ori_w, 1), dtype=np.uint8)*G_value*stage,
# #         np.ones((ori_h, ori_w, 1), dtype=np.uint8)*R_value*stage
# #     ),
# #     axis=-1
# # )
# # image_ori[150:300, 150:300] = mask_img[150:300, 150:300]
# # # cv2.imshow('B', B)
# # # cv2.imshow('G', G)
# # # cv2.imshow('R', R)
# # cv2.imshow('ii', cv2.resize(image_ori[100:130, 80:110], (ori_w, ori_h)))
# # cv2.imshow('mask img', mask_img)
# # cv2.imshow('image_ori', image_ori)
# # cv2.waitKey()
#
# # img = np.zeros((1000, 1000, 3), dtype=np.uint8)
# # gap = 9
# # offset = 2
# # for i in range(1000//gap):
# #     cv2.line(img, (0, i*gap), (1000, i*gap+offset), (0, 0, 255), 1)
# # # boxes = []
# # # boxes.append([[100, 100], [300, 100], [300, 300], [100, 300]])
# # # boxes.append([[200, 100], [400, 100], [400, 300], [200, 300]])
# # # cv2.fillPoly(img, np.array(boxes), (0, 0, 255))
# # cv2.imshow('img', img)
# # cv2.waitKey()
#
# # a = [0, 1, 2]
# # b = ','.join(a)
#
# list = [1, 2, 3, 4, 5]
#
# b = ''.join(list)


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

    return image


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
    data_path = '/workspace/JuneLi/bbtv/SensedealImgAlg/WORKFLOW/CLS/TableCls/v0/test_out/my_imgs_3/noline/'

    hostname = "192.168.1.217"
    port = 10022
    username = "root"
    password = "123456"

    sftp, sftp_client = get_remote(hostname, port, username, password)

    image_name_list = sftp.listdir(data_path)

    for index, image_name in enumerate(image_name_list):
        # if not image_name.startswith('total_2_44.jpg'):
        #     continue
        print(image_name)
        image = get_image_label(sftp_client, data_path + image_name,
                                       data_path.replace('/images/', '/labels/') + image_name.replace('.jpg', '.txt'))

        # image = cv2.resize(image, (256, 256))
        cv2.imshow('image', image)
        cv2.waitKey()


if __name__ == '__main__':
    main()

