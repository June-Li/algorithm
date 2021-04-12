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

from settings import TABLE_SETTINGS
from utils import format_cell_text

def find_tables(page, table_settings=TABLE_SETTINGS):
    '''提取表格，待修改'''
    tables = page.find_tables(table_settings)
    return tables


def parse_table(table, v_offsets_sorted=None, h_offsets_sorted=None):
    '''提取表格文本''' 
    
    cell_text_list = []
    cell_texts = table.extract()
    rows = table.rows
    assert len(rows) == len(cell_texts)
    
    if v_offsets_sorted is None:
        v_offsets_sorted = sorted(set([c[1] for c in table.cells]).union(set(c[3] for c in table.cells)))
    if h_offsets_sorted is None:
        h_offsets_sorted = sorted(set([c[0] for c in table.cells]).union(set(c[2] for c in table.cells)))        
    
    for i, row in enumerate(rows):
        assert len(row.cells) == len(cell_texts[i])
        for j, (cell, cell_text) in enumerate(zip(row.cells, cell_texts[i])):
            if cell is None:
                continue
            x0 = v_offsets_sorted.index(cell[1])
            y0 = h_offsets_sorted.index(cell[0])
            x1 = v_offsets_sorted.index(cell[3])
            y1 = h_offsets_sorted.index(cell[2])
            cell_bbox = [x0, y0, x1, y1]
            cell_text_list.append(",".join([str(b) for b in cell_bbox]) + "|" + format_cell_text(cell_text))
    
    if len(cell_text_list) != 0:
        cell_text_list = ["<table>"] + cell_text_list + ["</table>"]
    table_text = "\n".join(cell_text_list)
    return table_text

