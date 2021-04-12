# -*- coding: UTF-8 -*-
import os
import argparse
import glob
from wand.image import Image
import cv2
import pdfplumber
import io
import numpy as np
from PIL import Image as PI


def load_data(input_data_dir):
    pdf_list = []
    pdf_name = []
    pdf_file = glob.glob(input_data_dir + '/*.pdf')
    pdf_file.extend(glob.glob(input_data_dir + '/*.PDF'))
    for category in pdf_file:
        if category.startswith('.'):
            continue
        pdf_dir = category[:-4]
        pdf_name.append(pdf_dir.split('/')[-1])
        pdf_list.append(category)
    return pdf_list, pdf_name


def change(t1, t2):
    if t1[0] >= t2[2]:
        return t1, t2, True
    if t2[0] >= t1[2]:
        return t2, t1, False
    return t1, t2, True


def get_boxes(page, scale=1):
    text_box = []  # 文本的bbox[[x1,y1,x2,y2]]
    text_content = []
    blocks = page.extract_words()
    img = page.images
    if len(img) > 0:
        return [], [], False
    base = 0
    if blocks:
        for block in blocks:
            tmp = list(map(int, [block['x0'], block['top'], block['x1'], block['bottom']]))
            if tmp[3] - base > 10:
                text_box.append(tmp)
                base = tmp[3]
                text_content.append(block['text'])
            else:
                tmp2 = text_box[-1]
                tmp1, tmp2, flag = change(tmp, tmp2)
                if tmp1[0] - tmp2[2] > 10:
                    text_box.append(tmp)
                    text_content.append(block['text'])
                else:
                    new = [min(tmp1[0], tmp2[0]),
                           min(tmp1[1], tmp2[1]),
                           max(tmp1[2], tmp2[2]),
                           max(tmp1[3], tmp2[3])]
                    text_box[-1] = new
                    if flag:
                        text_content[-1] = text_content[-1] + block['text']
                    else:
                        text_content[-1] = block['text'] + text_content[-1]
                    base = (tmp[3] + base) // 2
    text_box = np.array(np.array(text_box) * scale, dtype=np.int)
    if len(text_box) < 1:
        return [], [], False
    else:
        text_box = text_box[text_box[:, 1].argsort()]
        text_content = np.array(text_content)[text_box[:, 1].argsort()]
        return text_box, text_content, True


def get_text(pdfpath, output_data_dir, resolution_para=200):
    image_pdf = Image(filename=pdfpath, resolution=resolution_para)
    conv = image_pdf.convert('jpg')
    pdf = pdfplumber.open(pdfpath)
    index = 0
    for img in conv.sequence:
        page = pdf.pages[index]
        if len(page.extract_words()) > 0:
            if not os.path.exists(output_data_dir):
                os.mkdir(output_data_dir)
            img_page = Image(image=img).make_blob('jpg')
            img = io.BytesIO(img_page)
            img = np.array(PI.open(img).convert('RGB'))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            height, weight = page.height, page.width
            radio = np.shape(img)[0] / height

            boxes, contents, flag = get_boxes(page, radio)
            if flag:
                label_txt_file = open(os.path.join(output_data_dir, str(index) + '.txt'), 'a+')
                for count_, box in enumerate(boxes):
                    out_str = ','.join(
                        [str(box[0]), str(box[1]), str(box[2]), str(box[1]), str(box[2]), str(box[3]), str(box[0]),
                         str(box[3]), contents[count_]])
                    label_txt_file.writelines(out_str + '\n')
                cv2.imwrite(os.path.join(output_data_dir, str(index) + '.jpg'), np.array(img, dtype=np.uint8))

        index += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        type=str,
        default='./pdf',
        help="input data directory"
    )
    parser.add_argument(
        '--output',
        dest='output',
        type=str,
        default='./img',
        help="output directory"
    )
    parser.add_argument(
        '--size',
        dest='size',
        type=int,
        default=0,
        help="Number of pdf in each file. size=0 refers to all file"
    )
    options = parser.parse_args()
    a = os.path.abspath('./pdf')
    input_data_dir = os.path.abspath(options.input)
    output_data_dir = os.path.abspath(options.output)
    num_per_class = options.size
    data_list, data_name_list = load_data(input_data_dir)
    # print(data_list, data_name_list)
    exit_name_list = os.listdir(output_data_dir)
    count = 0
    for i, fname in enumerate(data_list):
        if data_name_list[i] in exit_name_list:
            continue
        get_text(data_list[i], os.path.join(output_data_dir, data_name_list[i]), 200)
        count += 1
        if count % 100 == 0:
            print('processed num: ', count)
