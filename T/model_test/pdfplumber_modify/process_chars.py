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

from decimal import Decimal
from operator import itemgetter
from pdfplumber.utils import to_list
from settings import X_TOLERANCE, PARA_TOLERANCE_PERCENT, PAGE_PARA_TOLERANCE_PERCENT, LINE_CHAR_TOLERANCE
from layout_utils import line_chars_to_text
import logging
logging.getLogger(__name__)


def cluster_chars(chars):
    '''对chars进行分行聚类'''
    if len(chars) == 0:
        return []
    if len(chars) == 1:
        if chars[0]["text"][0] == " ":
            return []
        else:
            return [chars]
    
    groups = []
    chars = list(sorted(chars, key=itemgetter("doctop")))
    current_group = [chars[0]]
    last = chars[0]
    for char in chars[1:]:
        # 下一个字符的上边界大于上一个字符的下边界就换行
        if char["top"] <= last["bottom"]:
            current_group.append(char)
        else:
            groups.append(current_group)
            current_group = [char]
        last = char
    groups.append(current_group)
    
    # 删除全是空字符的行
    final_groups = []
    for group in groups:
        is_all_space = True
        for char in group:
            if char["text"][0] != " ":
                is_all_space = False
                break
        if not is_all_space:
            final_groups.append(group)
 
    return final_groups


def collate_line_chars(chars, tolerance=X_TOLERANCE):
    '''对每一行的chars按照x0进行排序'''
    tolerance = Decimal(tolerance)
    coll = []
    last_x1 = None
    chars_sorted = sorted(chars, key=itemgetter("x0"))
    
    # 删除最后一个为空的字符
    while True:
        if chars_sorted[-1]["text"][0] == " ":
            chars_sorted.pop(-1)
        else:
            break
    
    # 添加空格
    for char in chars_sorted:
        if (last_x1 is not None) and (char["x0"] > (last_x1 + tolerance)):
            coll.append(" ")
        last_x1 = char["x1"]
        coll.append(char)
    return coll


def segment_to_lines(segments, x_tolerance=X_TOLERANCE):
    '''对含有chars的块进行分行'''
    segment_lines = []
    
    for segment in segments:
        if not isinstance(segment, list):
            segment_lines.append(segment)
        elif len(segment) == 0:
            segment_lines.append(segment)
        else:
            chars = to_list(segment)
            clusters = cluster_chars(chars)
            line_chars = [collate_line_chars(cluster, x_tolerance) for cluster in clusters]
            segment_lines.append(line_chars)
    return segment_lines
        

def collate_para_chars(line_chars, page_bbox, tolerance=PARA_TOLERANCE_PERCENT, 
                       page_tolerance=PAGE_PARA_TOLERANCE_PERCENT, line_char_tolerance=LINE_CHAR_TOLERANCE):
    '''段落换行输出'''
    # if len(line_chars) == 0:
    #     return []
    # if len(line_chars) == 1:
    #     return line_chars

    if line_chars == 0:
        return []
    if line_chars == 1:
        return line_chars

    page_width = page_bbox[2] - page_bbox[0]
    tolerance = Decimal(tolerance)
    page_tolerance = Decimal(page_tolerance)
    line_char_tolerance = Decimal(line_char_tolerance)
    
    # 分段要求：1、一行以常见符号结束；2、是该页最后一行；
    #         3、该行最后一个字符小于该部分中所有chars的x1*阈值
    #         4、该行第一个字符的size和上一行最后一个字符的size差距大于阈值，则上一行分段
    #         4、该行最后一个字符大于该部分中所有chars的x1*阈值但下一行的第一个字符不小于该部分中所有chars的x0*阈值
    # 不分段标准：1、该行最后一个字符大于该部分中所有chars的x1*阈值且下一行的第一个字符小于该部分中所有chars的x0*阈值
    #           2、如果之前的行中存在没有匹配的"《 "或者"（"或者"("，就不分段
    #           3、上一行最后一个字符与last_min_x1的差值小于该行非中文字符串的长度则不分段
    page_char_min_x0 = min([line[0]["x0"] for line in line_chars])
    page_char_max_x1 = max([line[-1]["x1"] for line in line_chars])
    tolerance_width = tolerance * (page_char_max_x1 - page_char_min_x0)
    first_max_x0 = page_char_min_x0 + tolerance_width
    last_min_x1 = max((page_char_max_x1 - tolerance_width), page_tolerance*page_width)

    # 左书名号和左括号的数目，初始为0
    left_quotationmarks,left_cn_brackets,left_en_brackets=0,0,0

    paras = []
    para = []
    flag=True
    str_len=-1
    last_len=-1
    for i, line in enumerate(line_chars):
        collate_flag=False
        size_flag=True
        if len(line) == 0:
            continue

        if i>0:
            last_line=line_chars[i-1]
            for char in last_line:
                if char == " ":
                    continue
                if char["text"][0]== " ":
                    continue
                if char["text"] == "(":
                    left_en_brackets += 1
                if char["text"] == "（":
                    left_cn_brackets+=1
                if char["text"]=="《":
                    left_quotationmarks+=1
                if char["text"] == ")":
                    left_en_brackets -= 1
                if char["text"] == "）":
                    left_cn_brackets-=1
                if char["text"]=="》":
                    left_quotationmarks-=1
                # assert left_quotationmarks>-1 and left_brackets>-1

            if left_en_brackets > 0 or left_quotationmarks > 0 or left_cn_brackets>0:
                para.append(last_line)
                if i==len(line_chars)-1:
                    flag=False
                    para.append(line)
                    paras.append(para)
                    para=[]
                    break
                continue

            if last_line[-1]["text"] in ["。", "！", "：", ":", "？"]:
                para.append(last_line)
                paras.append(para)
                para = []
                if i==len(line_chars)-1:
                    flag=False
                    para.append(line)
                    paras.append(para)
                    para=[]
                    break
                continue

            have_han = False
            # 判断当前行和上一行是否是同一段落
            for char in line:
                if char == " ":
                    continue
                if char["text"][0]== " ":
                    continue
                # # 判断当前行和上一行的字体大小是否在阈值范围内，如果不在则分段
                # if size_flag and abs(char["size"] - last_line[-1]["size"]) > line_char_tolerance:
                #     para.append(last_line)
                #     paras.append(para)
                #     para = []
                #     collate_flag=True
                #     size_flag=False
                #     break

                if ('\u4e00' <= char["text"] <= '\u9fff'):
                    str_len = float(char["x0"]) - float(line[0]["x0"])
                    last_len = float(page_char_max_x1) - float(last_line[-1]["x1"])
                    have_han=True
                    break

            if not collate_flag:
                if not have_han:
                    str_len = float(line[-1]["x0"]) - float(line[0]["x0"])
                    last_len = float(page_char_max_x1) - float(last_line[-1]["x1"])
                if str_len>last_len:
                    # 当前行和上一行应该为同一段落
                    para.append(last_line)
                elif last_line[-1]["x1"]<=last_min_x1:
                    # 判断上一行最后一个字符是否小于该部分中所有chars的x1*阈值,若是则分段
                    para.append(last_line)
                    paras.append(para)
                    para=[]
                elif last_line[-1]["x1"]>last_min_x1:
                    para.append(last_line)

        # if i == len(line_chars) - 1:
        #     para.append(line)
        #     paras.append(para)
        #     para = []
        # 判断最后一行数据是否满足分段条件
        if i==len(line_chars)-1:
            para.append(line)
            paras.append(para)
            para = []
            if left_quotationmarks>0 or left_cn_brackets>0 or left_en_brackets>0:
                flag=True
            # if line[-1]["x1"]>last_min_x1*Decimal(0.9):
            if line[-1]["x1"]>page_char_max_x1*Decimal(0.9):
                flag=True
            last_len=float(page_char_max_x1) - float(line[-1]["x1"])

    if ('\u4e00' <= paras[-1][-1][-1]["text"] <= '\u9fff' ):
        flag=True
    if paras[-1][-1][-1]["text"] in ["。", "！", "：", ":", "？"]:
        flag=False

    return paras,flag,last_len,str_len


def extract_para_text(para):
    '''提取段落'''
    text = ""
    for line in para:
        text += line_chars_to_text(line)
    return text