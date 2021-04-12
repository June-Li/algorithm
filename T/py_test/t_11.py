import os
import shutil
import cv2
import numpy as np


def get_rotate_crop_image(img, points):
    # points = np.array(
    #     [[points[0], points[1]], [points[2], points[3]], [points[4], points[5]], [points[6], points[7]]],
    #     np.float32)
    points = np.array(points, np.float32)
    img_crop_width = int(
        max(
            np.linalg.norm(points[0] - points[1]),
            np.linalg.norm(points[2] - points[3])))
    img_crop_height = int(
        max(
            np.linalg.norm(points[0] - points[3]),
            np.linalg.norm(points[1] - points[2])))
    pts_std = np.float32([[0, 0], [img_crop_width, 0],
                          [img_crop_width, img_crop_height],
                          [0, img_crop_height]])
    M = cv2.getPerspectiveTransform(points, pts_std)
    dst_img = cv2.warpPerspective(
        img,
        M, (img_crop_width, img_crop_height),
        borderMode=cv2.BORDER_REPLICATE,
        flags=cv2.INTER_CUBIC)
    dst_img_height, dst_img_width = dst_img.shape[0:2]
    if dst_img_height * 1.0 / dst_img_width >= 1.5:
        dst_img = np.rot90(dst_img)
    return dst_img


base_path = '/workspace/JuneLi/bbtv/data_generator/Generate_det_rec/together/images/'
# base_path = '/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_14/test_1/'
image_name_list = os.listdir(base_path + 'images')
count = 0
for image_name in image_name_list:
    if not image_name.endswith('.jpg'):
        continue
    image_ori = cv2.imread(base_path + 'images/' + image_name)
    image_show = image_ori.copy()
    label_path = base_path + 'labels/' + image_name.replace('.jpg', '.txt')

    lines = open(label_path, 'r').readlines()
    for line in lines:
        box = line.split(',')[:8]
        box = [int(i) for i in box]
        points = np.array([[box[0], box[1]], [box[2], box[3]], [box[4], box[5]], [box[6], box[7]]])
        image_show = cv2.polylines(image_show, np.array([points]), True, (0, 255, 255), 2)
        image = get_rotate_crop_image(image_ori, points)

        h, w = np.shape(image)[0], np.shape(image)[1]
        image = cv2.resize(image, (32 * w // h, 32))
        h, w = np.shape(image)[0], np.shape(image)[1]
        if w > 1280:
            image = cv2.resize(image, (1280, 32))
        else:
            mask_img = np.ones((32, 1280, 3), dtype=np.uint8) * int(np.argmax(np.bincount(image.flatten(order='C'))))
            random_start = np.random.randint(0, 1280 - w)
            print(random_start, w, np.shape(image))
            mask_img[:, random_start:random_start + w] = image
            image = mask_img

        image_180 = np.rot90(image)
        image_180 = np.rot90(image_180)

        cv2.imshow('0', image)
        cv2.imshow('1', image_180)
        cv2.waitKey()
        if count % 100 == 0:
            cv2.imwrite('/workspace/JuneLi/bbtv/pytorch-cifar100/data/ocr_angle/test/0/' + str(count) + '.jpg', image)
            cv2.imwrite('/workspace/JuneLi/bbtv/pytorch-cifar100/data/ocr_angle/test/1/' + str(count) + '.jpg', image_180)
        elif count % 100 == 50:
            cv2.imwrite('/workspace/JuneLi/bbtv/pytorch-cifar100/data/ocr_angle/val/0/' + str(count) + '.jpg', image)
            cv2.imwrite('/workspace/JuneLi/bbtv/pytorch-cifar100/data/ocr_angle/val/1/' + str(count) + '.jpg', image_180)
        else:
            cv2.imwrite('/workspace/JuneLi/bbtv/pytorch-cifar100/data/ocr_angle/train/0/' + str(count) + '.jpg', image)
            cv2.imwrite('/workspace/JuneLi/bbtv/pytorch-cifar100/data/ocr_angle/train/1/' + str(count) + '.jpg', image_180)
        count += 1
        if count % 100 == 0:
            print('processed num: ', count)
