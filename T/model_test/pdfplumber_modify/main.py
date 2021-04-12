#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################
#                                                           
# Copyright (C) 2020 SenseDeal AI, Inc. All Rights Reserved 
#    
# Description:
#   pass
#
# Author: Li Xiuming & Li Lin
# Last Modified: 2020-10-29                                                 
############################################################

import random
import logging
logging.basicConfig(level=logging.ERROR)

import os
import time
from extract import Extract
import pdfplumber as pp
from tqdm import tqdm


if __name__ == "__main__":
    
    # from optparse import OptionParser
    # #parser = OptionParser()
    # parser.add_option("-i", "--input_dir", action="store", dest="input_dir")
    # parser.add_option("-o", "--output_dir", action="store", dest="output_dir",default=None)
    # options, args = parser.parse_args()
    # input_dir = options.input_dir
    # output_dir = options.output_dir

    # import sys
    # input_dir = sys.argv[1]
    # output_dir = os.path.join(input_dir, "txt")
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)

    input_dir = "./test_data"
    # # # input_dir = "/data/IE/htw/pdf_extractor/pdf_file"
    output_dir = "./result"
    input_dir="../get_pdf/pdf_data"
    # input_dir="./pdf_file"
    # filepath = "./test_data/AN201901031281665377.pdf"
    #filepath = "./test_data/AN201202270004250912.pdf"
    #filepath = "./test_data/临时报告（表格）3.pdf"

    filelist = os.listdir(input_dir)
    for filename in tqdm(filelist):
        # filename="AN201601290013311338.pdf"
        # filename="临时报告（表格）3.pdf"
        # filename="AN201901031281665377.pdf"
        # filename="1.案例1基金基金合同.pdf"
        # filename="AN201504300009438107.pdf"
        # filename="AN201604220014480732.pdf"
        # filename="03a72394-ed19-5c83-92f3-13dd96ba0965.pdf"
        filepath = os.path.join(input_dir, filename)
        if not filename.endswith("pdf") and not filename.endswith("PDF"):
            # print("Is it really a .pdf file?", filename)
            continue

        start_time = time.time()
        try:
            pdf = pp.open(filepath)
        except:
            print("Failed to open file:", filename)
            continue

        # extractor = Extract(pdf)
        # extractor.extract(keep_meta=True)
        # extractor.extract_text(output_header=True, output_pagenum=True, output_catalog=True)

        try:
            extractor = Extract(pdf)
            extractor.extract(keep_meta=True)
            extractor.extract_text(output_header=True, output_pagenum=True, output_catalog=True)
        except Exception as e:
            print(e, filename)
            continue

        pdf.close()
        end_time = time.time()
        used_time = end_time - start_time
        if used_time > 10.0:
            print("Long time consumed:", used_time)

        output_filepath = os.path.join(output_dir, filename.replace("pdf", "txt").replace("PDF", "txt"))
        with open(output_filepath, "w") as f:
            f.write(extractor.txt)
        # break
### 测验
    # input_dir = "../get_pdf/pdf_data"
    #
    # output_dir = "./result"
    # # filepath = "./test_data/AN201901031281665377.pdf"
    # # filepath = "./test_data/AN201202270004250912.pdf"
    # # filepath = "./test_data/临时报告（表格）3.pdf"
    #
    # filelist = os.listdir(input_dir)
    # file_idx=random.sample(range(len(filelist)),200)
    #
    # for idx in tqdm(file_idx):
    #     filename=filelist[idx]
    #     filepath = os.path.join(input_dir, filename)
    #     if not filename.endswith("pdf") and not filename.endswith("PDF"):
    #         print("Is it really a .pdf file?", filename)
    #         continue
    #
    #     start_time = time.time()
    #     try:
    #         pdf = pp.open(filepath)
    #     except:
    #         print("Failed to open file:", filename)
    #         continue
    #
    #     try:
    #         extractor = Extract(pdf)
    #         extractor.extract(keep_meta=True)
    #         extractor.extract_text(output_header=False, output_pagenum=False, output_catalog=False)
    #     except Exception as e:
    #         print(e, filename)
    #         continue
    #
    #     pdf.close()
    #     end_time = time.time()
    #     used_time = end_time - start_time
    #     if used_time > 10.0:
    #         print("Long time consumed:", used_time)
    #
    #     output_filepath = os.path.join(output_dir, filename.replace("pdf", "txt").replace("PDF", "txt"))
    #     with open(output_filepath, "w") as f:
    #         f.write(extractor.txt)