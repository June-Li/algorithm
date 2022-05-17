"""
result = 景图印黑 + 景黑印花
景黑印花 = α·景黑字原 + β·景黑印原  # α + β = 1
景黑字原 = 原图 * 景黑印白（1）

注：
    景黑印白是指印章之外的是0，印章处是1，是二值化到0和1的
    花是指叠加后的图像值
"""
import os
import cv2
import copy
import numpy as np


def resize_seal(img):
    try:
        h, w, _ = np.shape(img)
    except:
        h, w = np.shape(img)
    if h > 200 or w > 200:
        if h > w:
            img = cv2.resize(img, (200 * w // h, 200))
        else:
            img = cv2.resize(img, (200, 200 * h // w))
    # try:
    #     patch = np.ones((200, 200, 3), dtype=np.uint8)
    #     patch[:np.shape(img)[0], :np.shape(img)[1], :] = img
    # except:
    #     patch = np.ones((200, 200), dtype=np.uint8)
    #     patch[:np.shape(img)[0], :np.shape(img)[1]] = img
    return img


def g_seal(bg_img_path, seal_img_path, addweight_list, BGR2GRAY_FLAG):
    bg = cv2.imread(bg_img_path)
    bg_h, bg_w, _ = np.shape(bg)

    seal = cv2.imread(seal_img_path, 0)
    seal = resize_seal(seal)
    _, seal = cv2.threshold(seal, 200, 1, cv2.THRESH_BINARY)
    seal_bgr = cv2.cvtColor(seal, cv2.COLOR_GRAY2BGR)

    seal_h, seal_w = np.shape(seal)
    seal_inv = np.array(np.array(seal, dtype=float) * -1 + 1, dtype=np.uint8)
    seal_inv_bgr_b = cv2.cvtColor(seal_inv, cv2.COLOR_GRAY2BGR)

    seal_inv_bgr = seal_inv_bgr_b.copy()
    seal_inv_bgr[:, :, 0] = seal_inv_bgr_b[:, :, 0] * np.array(np.random.randint(0, 50, (seal_h, seal_w))*(np.random.randint(0, 10, (seal_h, seal_w))/10), dtype=np.uint8)
    seal_inv_bgr[:, :, 1] = seal_inv_bgr_b[:, :, 1] * np.array(np.random.randint(0, 50, (seal_h, seal_w))*(np.random.randint(0, 10, (seal_h, seal_w))/10), dtype=np.uint8)
    seal_inv_bgr[:, :, 2] = seal_inv_bgr_b[:, :, 2] * np.array(np.random.randint(150, 256, (seal_h, seal_w))*(np.random.randint(7, 10, (seal_h, seal_w))/10), dtype=np.uint8)

    bg_left_start, bg_up_start = np.random.randint(0, bg_w - seal_w), np.random.randint(0, bg_h - seal_h)
    bg_block = bg[bg_up_start:bg_up_start + seal_h, bg_left_start:bg_left_start + seal_w, :].copy()

    bg_black_ch_white = bg_block * seal_inv_bgr_b
    bg_white_seal_black = bg_block * seal_bgr

    seal_flower = cv2.addWeighted(bg_black_ch_white, addweight_list[0], seal_inv_bgr, addweight_list[1], 0)
    result = bg_white_seal_black + seal_flower

    if BGR2GRAY_FLAG:
        result = cv2.cvtColor(cv2.cvtColor(result, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

    return bg_block, result


def main():
    count = 0
    base_path = './'
    data_path = base_path + 'data/ori/train/'
    out_path = base_path + base_path + 'data/general/train/'
    bg_img_path_list = [data_path + 'bg/' + bg_img_path for bg_img_path in os.listdir(data_path + 'bg/')]
    seal_img_path_list = [data_path + 'seal/' + seal_img_path for seal_img_path in os.listdir(data_path + 'seal/')]
    for bg_img_path in bg_img_path_list:
        for seal_img_path in seal_img_path_list:
            for i in range(10):
                addweight_radio = round(np.random.randint(3, 10)/10, 1)
                while True:
                    seal_color_radio = [np.random.randint(0, 2), np.random.randint(0, 2), np.random.randint(0, 2)]
                    if sum(seal_color_radio) <= 2:
                        break
                bg_block, result = g_seal(bg_img_path,
                                          seal_img_path,
                                          [addweight_radio, 1 - addweight_radio],
                                          np.random.choice([True, False]))
                cv2.imwrite(out_path + 'bg/' + str(count) + '.jpg', bg_block)
                cv2.imwrite(out_path + 'seal/' + str(count) + '.jpg', result)
                # cv2.imshow('show img',
                #            np.hstack((bg_block, np.ones((np.shape(bg_block)[0], 10, 3), dtype=np.uint8)*0, result)))
                # key = cv2.waitKey()
                # if key == ord('q'):
                #     return
                count += 1
    print('general num: ', count)


if __name__ == '__main__':
    main()
