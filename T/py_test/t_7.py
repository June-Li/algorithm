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


def get_table(pdfpath, output_data_dir, resolution_para=200):
    # with image_pdf.convert('jpg') as conv:
    #     conv.save(filename=os.path.join(output_data_dir, 'page.jpg'))
    image_pdf = Image(filename=pdfpath, resolution=resolution_para)
    conv = image_pdf.convert('jpg')
    pdf = pdfplumber.open(pdfpath)
    index = 0
    for img in conv.sequence:
        page = pdf.pages[index]
        if len(page.find_tables()) > 0:
            if not os.path.exists(output_data_dir):
                os.mkdir(output_data_dir)
            img_page = Image(image=img).make_blob('jpg')
            img = io.BytesIO(img_page)
            img = np.array(PI.open(img).convert('RGB'))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            height, weight = page.height, page.width
            radio = np.shape(img)[0] / height
            cell_index = 0
            for table in page.find_tables():
                bbox = table.bbox  # x0, top, x1, bottom
                x0, y0, x1, y1 = int(bbox[0] * radio), int(bbox[1] * radio), int(bbox[2] * radio), int(
                    bbox[3] * radio)  # 左上右下
                cv2.imwrite(os.path.join(output_data_dir, str(index) + '_' + str(cell_index) + '.jpg'),
                            np.array(img[y0:y1, x0:x1], dtype=np.uint8))

                label_txt_file = open(os.path.join(output_data_dir, str(index) + '_' + str(cell_index) + '.txt'), 'a+')
                table_cells = table.cells
                for cell in table_cells:
                    cell_x0, cell_y0, cell_x1, cell_y1 = \
                        cell[0] * radio - x0, \
                        cell[1] * radio - y0, \
                        cell[2] * radio - x0, \
                        cell[3] * radio - y0
                    # if cell_x1 - cell_x0 < 20:
                    #     continue
                    w, h = x1 - x0, y1 - y0
                    cell_x_center, cell_y_center, cell_width, cell_height = \
                        round((cell_x0 + cell_x1) / 2 / w, 4), \
                        round((cell_y0 + cell_y1) / 2 / h, 4), \
                        round((cell_x1 - cell_x0) / w, 4), \
                        round((cell_y1 - cell_y0) / h, 4)
                    label_txt_file.writelines(' '.join(
                        ['0', str(cell_x_center), str(cell_y_center), str(cell_width), str(cell_height), '\n']))
                cell_index += 1
        index += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        type=str,
        # default='./pdf',
        default='/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_5/pdf',
        help="input data directory"
    )
    parser.add_argument(
        '--output',
        dest='output',
        type=str,
        default='/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_5/img',
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
    print(data_list, data_name_list)
    count = 0
    for i, fname in enumerate(data_list):
        get_table(data_list[i], os.path.join(output_data_dir, data_name_list[i]))
        count += 1
        if count % 100 == 0:
            print('processed num: ', count)
