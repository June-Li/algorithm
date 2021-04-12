#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################
#                                                           
# Copyright (C) 2020 SenseDeal AI, Inc. All Rights Reserved 
#    
# Description:
#   1.utils 改动了rect和image的to_edge
#
# Author: Li Xiuming
# Last Modified: 2020-10-29                                                 
############################################################

import logging
logging.getLogger(__name__)

from process_page import page_segment
from process_table import find_tables, parse_table
from process_meta import get_pages_meta
from process_chars import collate_para_chars,  segment_to_lines, extract_para_text


class Extract():
    def __init__(self, pdf):
        # 判断页数是否为0
        if len(pdf.pages) == 0:
            raise ValueError
            
        # 判断第一页字符是否为0，为扫描页
        if len(pdf.pages[0].chars) == 0:
            raise ValueError
        
        self.pdf = pdf
            
    def extract(self, keep_meta=True):
        self.pages_meta = None
        self.pages_segment_lines = []  
        self.pages_bbox = []
        
        # 页面分块
        for page in self.pdf.pages:
            tables = find_tables(page)            
            _, segments = page_segment(page, tables)
            segment_lines = segment_to_lines(segments)
            self.pages_segment_lines.append(segment_lines)
            self.pages_bbox.append(page.bbox)
    
        # 提取页面、页码、目录
        if keep_meta:
            self.pages_segment_lines, self.pages_meta = get_pages_meta(self.pages_segment_lines, self.pages_bbox)


    def extract_text(self, output_header=True, output_pagenum=True, output_catalog=True):
        '''提取文本'''
        text_list = []
        write_header = True
        write_pagenum = True
        merge_flag=False
        last_page_len=-1
        last_len=-1
        original_data=zip(self.pages_segment_lines, self.pages_bbox)
        for i, (segment_lines, page_bbox) in enumerate(original_data):

            # 页码
            if not merge_flag and i>0 and write_pagenum and output_pagenum and self.pages_meta is not None and i-1 in self.pages_meta["pagenums"] and \
                    self.pages_meta["pagenums"][i-1] is not None:
                pagenum_info = "\n".join(["<pagenum>"] + [self.pages_meta["pagenums"][i-1]] + ["</pagenum>"])
                text_list.append(pagenum_info)

            # 页眉
            if not merge_flag and output_header and self.pages_meta is not None and i in self.pages_meta["headers"] and self.pages_meta["headers"][i] is not None:
                header_info = "\n".join(["<header>"] + [self.pages_meta["headers"][i]] + ["</header>"])
                text_list.append(header_info)


            # 目录
            if output_catalog and self.pages_meta is not None and i in self.pages_meta["catalog"]["catalog_pagenums"] and self.pages_meta["catalog"]["catalog_text"] != "":
                catalog_info = "\n".join(["<catalog>"] + [self.pages_meta["catalog"]["catalog_text"]] + ["</catalog>"])
                text_list.append(catalog_info)
                output_catalog=False

            # 正文            
            for obj in segment_lines:
                if not isinstance(obj, list):
                    table_text = parse_table(obj)
                    text_list.append(table_text)
                else:
                    if len(obj) == 0:
                        continue
                    paras,flag,last_len,str_len = collate_para_chars(obj, page_bbox)

                    if merge_flag and len(paras)>0:
                        # 合并
                        text_list[-1]="".join([text_list[-1],extract_para_text(paras[0])])
                        paras.pop(0)
                    # elif str_len>last_page_len and len(paras)>0:
                    #     text_list[-1]="".join([text_list[-1],extract_para_text(paras[0])])
                    #     paras.pop(0)

                    if len(paras)>0:
                        text_list.append("\n".join([extract_para_text(para) for para in paras]))

                    merge_flag=flag
                    last_page_len=last_len



                
        text = "\n".join(text_list)
        self.txt = text