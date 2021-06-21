import numpy as np
import cv2
import os

def get_rotate_crop_image(img, points):
    points = np.array(
        [[points[0], points[1]], [points[2], points[3]], [points[4], points[5]], [points[6], points[7]]],
        np.float32)
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
    # cv2.imwrite('/home/bbtv/CRNN/buffer/j.jpg', np.array(dst_img, dtype=np.uint8))
    return dst_img


base_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/yolov3_table_cells_train/data/images/'
image = cv2.imread(base_path + '14.jpg')
dst_img = get_rotate_crop_image(image, [28, 3, 665, 25, 710, 815, 5, 835])
cv2.imshow('image', image)
cv2.imshow('dst_img', dst_img)
# cv2.imwrite(base_path + '14-1.jpg', dst_img)
cv2.waitKey()
