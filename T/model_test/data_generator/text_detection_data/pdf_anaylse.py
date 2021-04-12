import pdfplumber
import numpy as np
import cv2
import glob
import os
import random


def change(t1, t2):
    if t1[0] >= t2[2]:
        return t1, t2
    if t2[0] >= t1[2]:
        return t2, t1
    return t1, t2


def text_area_conf(table_arr, bbox):
    for area in table_arr:
        if bbox[1] >= area[0] and bbox[3] <= area[1]:
            return True
    return False


def draw_boxes(img_dir, bboxes):
    img = cv2.imread(img_dir)
    for bbox in bboxes:
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color=(0, 255, 0))
    return img


def get_img_scale(pdf_dir, output_dir, resolution=None):
    pdf_split = pdf_dir.split('/')
    pdf_name = pdf_split[-1]
    start = len(glob.glob(os.path.join(output_dir, '*.jpg')))
    with pdfplumber.open(pdf_dir) as pdf:
        for page in pdf.pages:
            im = page.to_image(resolution=resolution)
            # file_name = pdf_split[-1][:-4] + '_page_' + str(start) + '.jpg'
            file_name = pdf_name[:-4] + '_page_' + str(start) + '.jpg'
            im.save(os.path.join(output_dir, file_name))
            start += 1
    # img = cv2.imread(os.path.join(output_dir, file_name))
    # size = img.shape
    # return size[0] / pdf.pages[0].height
    return 1


def write_bboxes(pdf_dir, output_dir, bboxes):
    pdf_split = pdf_dir.split('/')
    pdf_name = pdf_split[-1]
    start = len(glob.glob(os.path.join(output_dir, '*.txt')))
    # file_name = pdf_split[-1][:-4] + '_page_' + str(start) + '.txt'
    file_name = pdf_name[:-4] + '_page_' + str(start) + '.txt'
    with open(os.path.join(output_dir, file_name), 'w') as f:
        # f.write(str(len(bboxes)) + '\n')
        for bbox in bboxes:
            string = ' '.join(list(map(str, bbox)))
            f.write(string + '\n')
    return


def write_bboxes_classes(pdf_dir, output_dir, bboxes):
    pdf_split = pdf_dir.split('/')
    start = len(glob.glob(os.path.join(output_dir, '*.txt')))
    file_name = pdf_split[-1][:-4] + '_page_' + str(start) + '.txt'
    with open(os.path.join(output_dir, file_name), 'a') as f:
        for key in bboxes.keys():
            bbox = bboxes[key]
            for i in range(len(bbox)):
                tmp = list(map(str, bbox[i]))
                tmp.append(key)
                string = ' '.join(tmp)
                f.write(string + '\n')
    return


# def write_vision_img(img, pdf_dir, output_dir, bboxes):

def get_boxes(page, scale=1):
    # im = page.to_image()
    # im.save('test.jpg')
    text_box = []  # 文本的bbox[[x1,y1,x2,y2]]
    # 检测有无table
    blocks = page.extract_words()
    img = page.images
    if len(img) > 0:
        return [], False
    base = 0
    if blocks:
        for block in blocks:
            tmp = list(map(int, [block['x0'], block['top'], block['x1'], block['bottom']]))
            if tmp[3] - base > 10:
                text_box.append(tmp)
                base = tmp[3]
            else:
                tmp2 = text_box[-1]
                tmp1, tmp2 = change(tmp, tmp2)
                if tmp1[0] - tmp2[2] > 10:
                    text_box.append(tmp)
                else:
                    new = [min(tmp1[0], tmp2[0]),
                           min(tmp1[1], tmp2[1]),
                           max(tmp1[2], tmp2[2]),
                           max(tmp1[3], tmp2[3])]
                    text_box[-1] = new
                    base = (tmp[3] + base) // 2
    text_box = np.array(np.array(text_box) * scale, dtype=np.int)
    if len(text_box) < 1:
        return [], False
    else:
        text_box = text_box[text_box[:, 1].argsort()]
        return text_box, True


if __name__ == '__main__':
    pdf_in = '/home/sxs/djy/ctpn_data/pdf/orginal_pdf/'
    img_out = '/home/sxs/djy/ctpn_data/pdf/pdf_text/'
    wrong_img = '/home/sxs/djy/ctpn_data/pdf/wrong/'
    txt_out = '/home/sxs/djy/ctpn_data/pdf/pdf_text/'
    pdfs = glob.glob(os.path.join(pdf_in, '*pdf'))
    pdfs.extend(glob.glob(os.path.join(pdf_in, '*PDF')))
    count = 0
    for pdf_dir in pdfs:
        # resolution = random.randint(120, 180)
        # scale = get_img_scale(pdf_dir=pdf_dir, output_dir=img_out)
        pdf_split = pdf_dir.split('/')
        pdf_name = pdf_split[-1]
        with pdfplumber.open(pdf_dir) as pdf:
            print(pdf_name)
            for page in pdf.pages:
                im = page.to_image()
                scale = im.annotated.height / page.height
                text_box, flag = get_boxes(page=page, scale=scale)

                if flag:
                    file_name = pdf_name[:-4] + '_page_' + str(count) + '.jpg'
                    im.save(os.path.join(img_out, file_name))
                    label_file_name = pdf_name[:-4] + '_page_' + str(count) + '.txt'
                    with open(os.path.join(txt_out, label_file_name), 'w') as f:
                        for bbox in text_box:
                            string = ' '.join(list(map(str, bbox)))
                            f.write(string + '\n')
                else:
                    file_name = pdf_name[:-4] + '_wrong_page_' + str(count) + '.jpg'
                    im.save(os.path.join(wrong_img, file_name))
                count += 1
