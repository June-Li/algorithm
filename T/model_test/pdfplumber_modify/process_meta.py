#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################
#                                                           
# Copyright (C) 2020 SenseDeal AI, Inc. All Rights Reserved 
#    
# Description:
#   pass
#
# Author: Li Xiuming
# Last Modified: 2020-10-29                                                 
############################################################

import re
from decimal import Decimal
from utils import line_chars_to_text
from settings import PAGENUM_TOLERANCE, HEADER_TOLERANCE
from process_chars import extract_para_text
#import Levenshtein

# 得到当前页面中所有char的第2小的size
def get_min_page_size(segment_lines):
    min_size=100
    second_min_size=100
    max_size=0
    for segment_line in segment_lines:
        if not isinstance(segment_line,list):
            continue
        for line in segment_line:
            if second_min_size>line[0]["size"]:
                second_min_size=line[0]["size"]
                if second_min_size<min_size:
                    min_size,second_min_size=second_min_size,min_size
            if max_size<line[0]["size"]:
                max_size=line[0]["size"]
    return min_size,second_min_size,max_size

def get_possible_header(segment_lines, page_bbox, tolerance=HEADER_TOLERANCE):
    '''找到第一行作为可能的页眉，取出第一块第一行的text'''
    tolerance = Decimal(tolerance)

    if len(segment_lines) == 0: # 空页
        return None
    if not isinstance(segment_lines[0], list): # 第一块为表格
        return None
    if len(segment_lines[0]) == 0: # 第一块为空的
        return None
    if len(segment_lines[0][0]) == 0: # 第一块的第一行为空
        return None
    if segment_lines[0][0][0]["top"] >= Decimal(page_bbox[1] + Decimal(0.1) *(page_bbox[3]-page_bbox[1])):
        return None
    min_size,_,max_size=get_min_page_size(segment_lines)
    if segment_lines[0][0][0]["size"]>min_size+Decimal(1):
        return None
    if segment_lines[0][0][0]["size"]>=max_size-Decimal(0.5):
        return None
    line_text = line_chars_to_text(segment_lines[0][0])
    line_text = line_text.strip()
    if line_text == "":
        return None
    
    return line_text


def get_possible_pagenum(segment_lines, page_bbox, tolerance=PAGENUM_TOLERANCE):

    '''找到最后一行作为可能的页码，取出最后一块最后一行的text'''
    tolerance = Decimal(tolerance)
    
    if len(segment_lines) == 0: # 空页
        return None
    if not isinstance(segment_lines[-1], list): # 最后一块为表格
        return None
    if len(segment_lines[-1]) == 0: # 最后一块为空的
        return None
    if len(segment_lines[-1][-1]) == 0: # 最后一块的最后一行为空
        return None
    if segment_lines[-1][-1][-1]["bottom"] <= Decimal(page_bbox[3] - tolerance *(page_bbox[3]-page_bbox[1])):
        return None
    _, second_min_size, max_size = get_min_page_size(segment_lines)
    if segment_lines[-1][-1][-1]["size"]>second_min_size+Decimal(2):
        return None
    if segment_lines[-1][-1][-1]["size"]>=max_size-Decimal(0.5):
        return None
    # print(get_min_page_size(segment_lines))

    line_text = line_chars_to_text(segment_lines[-1][-1])
    line_text = line_text.strip()
    if line_text == "":
        return None
    
    if re.findall("[0-9页IVXLXCDM]+", line_text) == 0 or len(line_text.replace(" ", "")) > 8:
        return None
    
    return line_text


def is_headers(possible_headers,page_num):
    '''页眉总数应该大于所有页的1/2'''
    headers_list = [h for h in possible_headers if h is not None]
    if len(headers_list)>page_num/2:
        return True
    return False

    # '''去重后的可能页眉数目小于所有页的1/3则为页眉'''
    # headers_list = [h for h in possible_headers if h is not None]
    # headers_set = set(headers_list)
    # if len(headers_list) < 3:
    #     return False
    # elif len(headers_list) ==3:
    #     if len(headers_list) < 2:
    #         return False
    #     if len(headers_set) == 1:
    #         return True
    # else:
    #     if len(headers_set) < (1/3) * len(headers_list):
    #         return True
    # return False
def is_pagenums(possible_pagenums):
    '''去重后页数大于所有页的1/2则为页码'''

    pagenums_list = [n for n in possible_pagenums if n is not None]
    pagenums_set = set(pagenums_list)
    if len(pagenums_list) == 0:
        return False   
    else:
        if len(pagenums_set) < 0.9 * len(pagenums_list):
            return False
    
    return False

def is_title(line,max_size,page_width):
    if line[0]["size"]<max_size-Decimal(0.5):
        return False
    mid_position=(line[0]["x0"]+line[-1]["x1"])/2
    bias=line[0]["width"]*Decimal(0.5)
    if mid_position<page_width/2-bias or mid_position>page_width/2+bias:
        return False
    for char in line:
        if char==" ":
            continue
        if char["text"] in [",","，","。","!","！"]:
            return False
    return True

def get_headers(pages_segment_lines, pages_bbox):
    '''返回所有的页眉'''
    possible_headers = [get_possible_header(segment_lines, page_bbox) for segment_lines, page_bbox in zip(pages_segment_lines, pages_bbox)]
    # return possible_headers
    is_pages_headers = is_headers(possible_headers,len(pages_segment_lines))
    if is_pages_headers:
        return possible_headers
    else:
        return None

def get_pagenums(pages_segment_lines, pages_bbox):
    '''返回所有的页码'''
    possible_pagenums = [get_possible_pagenum(segment_lines, page_bbox) for segment_lines, page_bbox in zip(pages_segment_lines, pages_bbox)]

    return possible_pagenums

    # is_pages_pagenums = is_pagenums(possible_pagenums)
    # if is_pages_pagenums:
    #     return possible_pagenums
    # else:
    #     return None

def get_catalog(pages_segment_lines):
    '''获取目录'''
    catalog_pagenums = [] 
    
    catalog_mark = False
    catalog_symbol = None
    for i, segment_lines in enumerate(pages_segment_lines):
        # 只考虑前5页
        if i > 4:
            break
        # 只考虑只有一个块且不是表格的页
        if len(segment_lines) != 1 or not isinstance(segment_lines, list):
            # 如果上一页是目录，则这一页直接break
            if catalog_mark:
                break
            else:
                continue
        # 只考虑第一块
        for j, line in enumerate(segment_lines[0]):
            # 只考虑前5句
            if j > 4:
                break
            line_text = line_chars_to_text(line).replace(" ", "")
            if re.sub(" +", "", line_text) == "目录":
                catalog_mark = True
                line_text = line_chars_to_text(segment_lines[0][j+1]).replace(" ", "")
                catalog_symbol = re.sub("[0-9A-Za-z\u4e00-\u9fa5]", "", line_text)
                # 取出最大个数的符号
                catalog_symbol = max(catalog_symbol, key=catalog_symbol.count)
                break
            elif catalog_mark and catalog_symbol is not None and 5*catalog_symbol in line_text:  
                # 上一页是目录，这一页也是
                break
            else:
                catalog_mark = False

        if catalog_mark:
            catalog_pagenums.append(i)
            break
        
    return catalog_pagenums

        
def get_pages_meta(pages_segment_lines, pages_bbox):
    '''存储所有页面的页眉，页码，目录'''
    pages_meta = {"headers": {}, "pagenums": {}, "catalog": {"catalog_pagenums": [], "catalog_text": ""}}
        
    # 获取页眉
    headers = get_headers(pages_segment_lines, pages_bbox)
    # 获取页码
    pagenums = get_pagenums(pages_segment_lines, pages_bbox)  
    # 获取目录
    catalog_pagenums = get_catalog(pages_segment_lines)
    if headers is not None:
        pages_meta["headers"] = {i:headers[i] for i in range(len(headers))}
    if pagenums is not None:
        pages_meta["pagenums"] = {i:pagenums[i] for i in range(len(pagenums))}
    pages_meta["catalog"]["catalog_pagenums"] = catalog_pagenums
      
    # 移动页眉、页码、目录到meta信息里
    catalog_text = []
    for i, segment_lines in enumerate(pages_segment_lines):
        if len(segment_lines) == 0:
            continue
        if headers is not None and headers[i] is not None:
            segment_lines[0].pop(0)
        if pagenums is not None and pagenums[i] is not None:
            segment_lines[-1].pop(-1)
        # 删除掉页眉页码之后再提取目录
        if i in catalog_pagenums:
            catalog_text.extend([line_chars_to_text(line) for line in segment_lines[0]])
            pages_segment_lines[i] = []

        # 删掉页眉页码目录之后再提取标题
        if i<2:
            title=[]
            if len(segment_lines) == 0:
                continue
            if not isinstance(segment_lines[0],list):
                continue
            min_size, _, max_size = get_min_page_size(segment_lines)
            for n,line in enumerate(segment_lines[0]):
                if len(line)==0:
                    continue
                if is_title(line,max_size,pages_bbox[i][2]):
                    if len(title)>0:
                        # 判断当前行与上一行是否是属于同一标题
                        last_bottom=segment_lines[0][n-1][0]["bottom"]
                        cur_top=line[0]["top"]

                        if (cur_top-last_bottom)<line[0]["height"]+min_size*Decimal(0.5):
                            title.append(line)
                        else:break
                    # 当前行若非本页第一行则：当前行与上一行的行间距>当前行字体的height*Demical(2)
                    elif n>0:

                        last_bottom = segment_lines[0][n - 1][0]["bottom"]
                        cur_top = line[0]["top"]
                        if (cur_top-last_bottom)>line[0]["height"]*Decimal(2):
                            title.append(line)
                    else:
                        title.append(line)
                elif len(title)>0:
                    break

            if title is not None:
                ssss="".join([line_chars_to_text(line) for line in title])
                print(i,ssss)

    pages_meta["catalog"]["catalog_text"] = "\n".join(catalog_text)
    return pages_segment_lines, pages_meta