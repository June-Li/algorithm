# -*- coding: utf-8 -*-
# @Time    : 2022/4/6 14:56
# @Author  : lijun
import cv2
import os
import numpy as np
import torch
from math import fabs, sin, cos, radians
import time
import copy
import xlsxwriter
from docx import Document


class TableStructure:
    def __init__(self):
        pass

    def table_structure(self, boxes, text_list, out_dir=None):
        """

        :param boxes: [[row_up, col_left, row_down, col_right], ……]
        :param text_list: ['hello', 'world', ……]
        :param out_dir: 生成html的输出位置
        :return:
        """
        if out_dir:
            # 写入html开始
            max_row = np.max(np.array(boxes)[:, [2]])
            max_col = np.max(np.array(boxes)[:, 3])
            html_table_list = []
            for i in range(max_row):
                html_h_list = []
                for j in range(max_col):
                    html_h_list.append('')
                html_table_list.append(html_h_list)

            index = 0
            for box in boxes:
                x_0, y_0, x_1, y_1 = box[1], box[0], box[3], box[2]
                cell_str = '<td '
                cell_str = cell_str + 'class=' + '"' + 'tg-0lax' + '" '
                cell_str = cell_str + 'rowspan=' + '"' + str(y_1 - y_0) + '" '  # 向下融合cell的数量
                cell_str = cell_str + 'colspan=' + '"' + str(x_1 - x_0) + '" '  # 向右融合cell的数量
                # cell_str = cell_str + 'height=' + '"' + str(box[3] - box[1]) + '" '  # 设置cell的宽
                # cell_str = cell_str + 'width=' + '"' + str(box[2] - box[0]) + '" '  # 设置cell的高
                cell_str = cell_str + '>'
                cell_str = cell_str + text_list[index].replace('<***۞Enter۞***>', '<br>')  # 文本内容
                cell_str = cell_str + '</td>'  # 结束符
                html_table_list[y_0][x_0] = cell_str
                index += 1
            html_file = open(out_dir, 'w')
            html_file.write(self.html_configuration()[0])
            for i in html_table_list:
                if i == [''] * len(i):
                    continue
                html_file.write('<tr>\n')
                for j in i:
                    if j != '':
                        html_file.write(j + '\n')
                html_file.write('</tr>\n')
            html_file.write(self.html_configuration()[1])
            html_file.close()

    def html_configuration(self):
        html_head = '<!DOCTYPE html>\n' + \
                    '<html lang="en">\n' + \
                    '<head>\n' + \
                    '    <meta charset="UTF-8">\n' + \
                    '    <title>Title</title>\n' + \
                    '</head>\n' + \
                    '<body>\n' + \
                    '<style type="text/css">\n' + \
                    '.tg  {border-collapse:collapse;border-spacing:0;}\n' + \
                    '.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;\n' + \
                    '  overflow:hidden;padding:10px 5px;word-break:normal;}\n' + \
                    '.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;\n' + \
                    '  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}\n' + \
                    '.tg .tg-0lax{text-align:left;vertical-align:top}\n' + \
                    '</style>\n' + \
                    '<table class="tg">\n' + \
                    '    <tbody>\n'
        html_tail = '    </tbody>\n' + \
                    '</table>\n' + \
                    '</body>\n' + \
                    '</html>\n'
        return [html_head, html_tail]


if __name__ == '__main__':
    TS = TableStructure()
    # data_ori = [
    #     [[0, 0, 1, 1], '华泰博远17号集合资产管理计划'],
    #     [[0, 1, 1, 2], '13, 000.00'],
    #     [[1, 0, 2, 1], '华泰如意宝邮发1号集合资产管理计划'],
    #     [[1, 1, 2, 2], '13, 000.00'],
    #     [[2, 0, 3, 1], '华泰紫金1号集合资产管理计划'],
    #     [[2, 1, 3, 2], '40, 000.00'],
    #     [[3, 0, 4, 1], '华泰紫金周期轮动集合资产管理计划'],
    #     [[3, 1, 4, 2], '10, 000.00']
    # ]
    # boxes, text_list = [], []
    # for elem in data_ori:
    #     boxes.append(elem[0])
    #     text_list.append(elem[1])

    boxes, text_list = [], []
    lines = open('../../T/txt_test/t_0.txt', 'r').readlines()
    for line in lines:
        boxes.append(list(eval(line.split('|', 1)[0])))
        text_list.append(line.split('|', 1)[-1].strip())
    TS.table_structure(boxes, text_list, './a.html')
