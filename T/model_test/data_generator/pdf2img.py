# -*- coding: UTF-8 -*-
import os
import argparse
import glob
from wand.image import Image


def load_data(input_data_dir):
    pdf_list = []
    pdf_name = []
    pdf_file = glob.glob(input_data_dir + '/*.pdf')
    pdf_file.extend(glob.glob(input_data_dir + '/*.PDF'))
    print(pdf_file)
    for category in pdf_file:
        if category.startswith('.'):
            continue
        pdf_dir = category[:-4]
        pdf_name.append(pdf_dir.split('/')[-1])
        pdf_list.append(category)
    return pdf_list, pdf_name


def Pdf2Image(pdfpath, output_data_dir, resolution_para=200):
    image_pdf = Image(filename=pdfpath, resolution=resolution_para)
    with image_pdf.convert('jpg') as conv:
        conv.save(filename=os.path.join(output_data_dir, 'page.jpg'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        type=str,
        default='input_pdf',
        help="input data directory"
    )
    parser.add_argument(
        '--output',
        dest='output',
        type=str,
        default='input_pdf',
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
    input_data_dir = options.input
    output_data_dir = options.output
    num_per_class = options.size
    data_list, data_dir = load_data(input_data_dir)
    print(data_list, data_dir)
    for i, fname in enumerate(data_list):
        Pdf2Image(data_list[i], os.path.join(output_data_dir, data_dir[i]))
