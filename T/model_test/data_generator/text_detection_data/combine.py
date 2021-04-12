import cv2
import numpy as np
import os
import math
import random
import glob


def crop(Img):
    H, W, z = Img.shape
    y = H / 2 + 20
    x = W / 2 + 60
    winW = random.randrange(100, x - 60)
    winH = random.randrange(80, y - 20)
    # cv2.rectangle(rotateImg, (int(x-winW), int(y-winH)), (int(x + winW), int(y + winH)), (0, 255, 0), 2)
    # cv2.imshow('tfimg',rotateImg)
    # cv2.waitKey(0)
    # cropImg_clone = rotateImg.copy()
    cropImg = Img[int(y - winH):int(y + winH), int(x - winW):int(x + winW), :]
    return cropImg


def rotate_bound(image, angle=1.5):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH), borderValue=(255, 255, 255))


if __name__ == '__main__':
    rootdir = '/home/sxs/djy/ctpn_data/pdf/'
    bg_list = glob.glob(os.path.join(rootdir, 'bg', '*.png'))
    seal_list = glob.glob(os.path.join(rootdir, 'seal'))
    num_bg = len(bg_list)
    num_seal = len(seal_list)
    bg = [cv2.imread(os.path.join(path)) for path in bg_list]
    seal = [cv2.imread(os.path.join(path)) for path in seal_list]
    txt_list = glob.glob(os.path.join(rootdir, 'pdf_text', '*.txt'))
    image_list = glob.glob(os.path.join(rootdir, 'pdf_text', '*.jpg'))
    i_cou = 0
    for path in txt_list:
        if i_cou % 1000 == 0:
            print(i_cou)
        i_cou += 1
        bboxs = []
        for line in open(path, 'r'):
            line = line.strip('\n')
            bboxs.append(list(map(int, line.split(' '))))
        if len(bboxs) <= 1:
            continue
        img_path = path[:-3] + 'jpg'
        orig_no = cv2.imread(img_path)
        h_o, w_o, z = orig_no.shape
        while True:
            alpha = random.normalvariate(0, 1)
            if -3 < alpha < 3:
                break
        theta = math.radians(alpha)
        orig = rotate_bound(orig_no, alpha)
        h, w, z = orig.shape
        select_bg = bg[random.randint(0, num_bg - 1)]
        select_bg = crop(select_bg)
        select_bg = cv2.resize(select_bg, (w, h))
        _, thresh1 = cv2.threshold(orig, 127, 255, cv2.THRESH_BINARY)
        index = np.where(thresh1 == 0)
        threshold = random.randint(120, 200)
        _, thresh1 = cv2.threshold(orig, threshold, 255, cv2.THRESH_BINARY)
        orig[np.where(thresh1 == 255)] = select_bg[np.where(thresh1 == 255)]
        shift_y, shift_x = abs((h - h_o)) // 2, abs((w - w_o)) // 2
        final = orig[shift_y:shift_y + h, shift_x:w - shift_x, :]
        img_name = img_path.split('/')[-1]
        cv2.imwrite(os.path.join(rootdir, 'new', img_name), final)
        new_box = []
        for box in bboxs:
            [x0, y0, x1, y1] = box
            tmp1 = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]
            center_x, center_y = (w) / 2.0, (h) / 2.0
            tmp = []
            for loc in tmp1:
                [x, y] = loc
                new_x = (x - center_x) * math.cos(theta) - (y - center_y) * math.sin(theta) + center_x
                new_y = (x - center_x) * math.sin(theta) + (y - center_y) * math.cos(theta) + center_y
                tmp.extend([int(new_x), int(new_y)])

            new_box.append([min(tmp[0], tmp[2], tmp[4], tmp[6]),
                            min(tmp[1], tmp[3], tmp[5], tmp[7]),
                            max(tmp[0], tmp[2], tmp[4], tmp[6]),
                            max(tmp[1], tmp[3], tmp[5], tmp[7])])
        with open(os.path.join(rootdir, 'new', img_name[:-4] + '.txt'), 'w') as f:
            for box in new_box:
                info = ' '.join(map(str, box))
                f.write(info + '\n')
