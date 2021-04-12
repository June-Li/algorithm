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

import collections
from operator import itemgetter
import logging
logging.getLogger(__name__)


def page_segment(page, tables):
    '''按照表格的top位置将一页中所有的chars分为多段，表格前，表格后'''
    
    # 提取页面内的字符
    chars = []
    for char in page.chars:
        if char["top"] < page.bbox[1]:
            logging.info("char's top is out of page's top.")
        elif char["bottom"] > page.bbox[3]:
            logging.info("char's botttom is out of page's bottom.")
        else:
            chars.append(char)
            
    # 如果没有表格
    if len(tables) == 0:
        return [(page.bbox[1], page.bbox[3])], [chars] # 空页也返回
    
    # 按表格边界将页面分割
    segments = collections.defaultdict(list)
    
    # 提取表格上下边界
    table_borders = []
    for table in tables:
        table_borders.append((table.bbox[1], table.bbox[3]))
        segments[(table.bbox[1], table.bbox[3])] = table
    table_borders = sorted(table_borders, key=lambda x: x[0])
    
    # 提取页面分块边界(不含表格内的字)
    borders = []
    for i, border in enumerate(table_borders):
        if i == 0:
            borders.append((page.bbox[1], border[0])) # 第一个table前
        else:
            borders.append((table_borders[i-1][1], border[0])) # 未到最后一个table, 两个表格之间
        if i == len(table_borders)-1:
            borders.append((border[1], page.bbox[3])) # 最后一个table后
    
    # 返回页面分割后每部分的chars
    for char in chars:
        for border in borders:
            if char["top"] >= border[0] and char["bottom"] < border[1]:
                segments[border].append(char)
                break
            
    segments_sorted = sorted(segments.items(), key=itemgetter(0))
    borders, segments = zip(*segments_sorted)
    return borders, segments














