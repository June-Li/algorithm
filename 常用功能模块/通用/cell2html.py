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

    def cal_iou(self, box_0, box_1, cal_type=-1):
        iou, overlap_area, flag = 0, 0, False
        min_x = min(box_0[0], box_0[2], box_1[0], box_1[2])
        max_x = max(box_0[0], box_0[2], box_1[0], box_1[2])
        min_y = min(box_0[1], box_0[3], box_1[1], box_1[3])
        max_y = max(box_0[1], box_0[3], box_1[1], box_1[3])
        box_0_w = abs(box_0[0]-box_0[2])
        box_0_h = abs(box_0[1]-box_0[3])
        box_1_w = abs(box_1[0]-box_1[2])
        box_1_h = abs(box_1[1]-box_1[3])
        merge_w = max_x - min_x
        merge_h = max_y - min_y
        overlap_w = box_0_w + box_1_w - merge_w
        overlap_h = box_0_h + box_1_h - merge_h
        if overlap_h > 0 and overlap_w > 0:
            box_0_area = box_0_w * box_0_h
            box_1_area = box_1_w * box_1_h
            overlap_area = overlap_w * overlap_h
            if cal_type == 0:
                iou = overlap_area / box_0_area
            elif cal_type == 1:
                iou = overlap_area / box_1_area
            else:
                iou = overlap_area / (box_0_area + box_1_area - overlap_area)
            if overlap_w > 10 or overlap_h > 10:
                flag = True
        return iou, flag

    def cal_iou_parallel(self, boxes_0, boxes_1, cal_type=-1):
        """
        NxM， boxes_0中每个框和boxes_1中每个框的IoU值；
        :param boxes_0: [[x_0, y_0, x_1, y_1], ……]，左上右右下角，N个
        :param boxes_1: [[x_0, y_0, x_1, y_1], ……]，左上右右下角，M个
        :return:
        """
        area_0 = (boxes_0[:, 2] - boxes_0[:, 0]) * (boxes_0[:, 3] - boxes_0[:, 1])  # 每个框的面积 (N,)
        area_1 = (boxes_1[:, 2] - boxes_1[:, 0]) * (boxes_1[:, 3] - boxes_1[:, 1])  # 每个框的面积 (M,)

        lt = torch.max(boxes_0[:, None, :2], boxes_1[:, :2])  # [N,M,2]
        rb = torch.min(boxes_0[:, None, 2:], boxes_1[:, 2:])  # [N,M,2]

        wh = (rb - lt).clamp(min=0)  # [N,M,2]  #小于0的为0  clamp 钳；夹钳；
        inter = wh[:, :, 0] * wh[:, :, 1]  # [N,M]

        if cal_type == -1:
            iou = inter / (area_0[:, None] + area_1 - inter)
        elif cal_type == 0:
            iou = inter / (area_0[:, None] + torch.zeros(area_1.shape[0], dtype=torch.float32, device=area_0.device))
        elif cal_type == 1:
            iou = inter / (torch.zeros(area_0.shape[0], dtype=torch.float32, device=area_1.device)[:, None] + area_1)
        else:
            raise ValueError
        return iou

    def find_connected(self, isConnected):
        """
        深度优先搜索算法，把相近的线划分为同一个连通域
        """
        def dfs(i: int, province_list):
            for j in range(provinces):
                if isConnected[i][j] == 1 and j not in visited:
                    visited.add(j)
                    province_list.append(j)
                    dfs(j, province_list)

        provinces = len(isConnected)
        visited = set()
        circles = 0
        provinces_list = []
        for i in range(provinces):
            if i not in visited:
                province_list = []
                dfs(i, province_list)
                circles += 1
                provinces_list.append(province_list)

        return circles, provinces_list

    def calculate_distance_threshold(self, boxes):
        dial_list = []
        height_list = []
        for i in range(100):
            dial_list.append(0)
            height_list.append([])
        for box in boxes:
            try:
                dial_list[int((abs(box[3] - box[1]))/50)] += 1
                height_list[int((abs(box[3] - box[1]))/50)].append(abs(box[3] - box[1]))
            except:
                dial_list[-1] += 1
                height_list[-1].append(abs(box[3] - box[1]))
        index = int(np.argmax(dial_list))
        distance_threshold = np.average(height_list[index])/3

        if distance_threshold < 20:
            return distance_threshold
        else:
            return 20

    def merge_h_lines(self, h_line, iou_threshold, distance_threshold, boxes):
        """
        深度优先搜索，所以先构建邻接矩阵
        """
        isConnected = np.zeros((len(h_line), len(h_line)))
        for index_one in range(len(h_line)):
            for index_two in range(len(h_line)):
                if index_two < index_one:
                    continue
                elif index_two == index_one:
                    isConnected[index_one][index_two] = 1
                    continue
                line_1 = h_line[index_one]
                line_2 = h_line[index_two]
                union = max(line_1[0][0], line_1[1][0], line_2[0][0], line_2[1][0]) - min(line_1[0][0], line_1[1][0],
                                                                                          line_2[0][0], line_2[1][0])
                total = abs(line_1[0][0] - line_1[1][0]) + abs(line_2[0][0] - line_2[1][0])
                intersect = total - union
                iou = intersect / union
                distance = abs(line_1[0][1] - line_2[0][1])  # / np.shape(image)[0]
                if iou > iou_threshold and distance < distance_threshold:
                    isConnected[index_one][index_two] = 1
                    isConnected[index_two][index_one] = 1
        circles, provinces_list = self.find_connected(isConnected)

        merge_h_line_list = []
        for province_list in provinces_list:
            x_set = []
            y_set = []
            for index in province_list:
                line = h_line[index]
                x_set.append(line[0][0])
                x_set.append(line[1][0])
                y_set.append(line[0][1])
            merge_h_line_list.append([[min(x_set), np.average(y_set)], [max(x_set), np.average(y_set)]])
            for index in province_list:
                if h_line[index][2][0] == 'up':
                    boxes[h_line[index][3]][1] = int(np.average(y_set))
                elif h_line[index][2][0] == 'down':
                    boxes[h_line[index][3]][3] = int(np.average(y_set))
                else:
                    raise ValueError

        merge_h_line_list = np.array(merge_h_line_list, dtype=np.int)

        for index_, box_ in enumerate(boxes):
            if box_[0] > box_[2]:
                boxes[index_][0] = box_[2]
                boxes[index_][2] = box_[0]
            if box_[1] > box_[3]:
                boxes[index_][1] = box_[3]
                boxes[index_][3] = box_[1]

        return merge_h_line_list, boxes

    def merge_v_lines(self, v_line, iou_threshold, distance_threshold, boxes):
        """
        深度优先搜索，所以先构建邻接矩阵
        """
        isConnected = np.zeros((len(v_line), len(v_line)))
        for index_one in range(len(v_line)):
            for index_two in range(len(v_line)):
                if index_two < index_one:
                    continue
                elif index_two == index_one:
                    isConnected[index_one][index_two] = 1
                    continue
                line_1 = v_line[index_one]
                line_2 = v_line[index_two]
                union = max(line_1[0][1], line_1[1][1], line_2[0][1], line_2[1][1]) - min(line_1[0][1], line_1[1][1],
                                                                                          line_2[0][1], line_2[1][1])
                total = abs(line_1[0][1] - line_1[1][1]) + abs(line_2[0][1] - line_2[1][1])
                intersect = total - union
                iou = intersect / union
                distance = abs(line_1[0][0] - line_2[0][0])  # / np.shape(image)[0]
                if iou > iou_threshold and distance < distance_threshold:
                    isConnected[index_one][index_two] = 1
                    isConnected[index_two][index_one] = 1

        circles, provinces_list = self.find_connected(isConnected)

        merge_v_line_list = []
        for province_list in provinces_list:
            x_set = []
            y_set = []
            for index in province_list:
                line = v_line[index]
                x_set.append(line[0][0])
                y_set.append(line[0][1])
                y_set.append(line[1][1])
            merge_v_line_list.append([[np.average(x_set), min(y_set)], [np.average(x_set), max(y_set)]])
            for index in province_list:
                if v_line[index][2][0] == 'left':
                    boxes[v_line[index][3]][0] = int(np.average(x_set))
                elif v_line[index][2][0] == 'right':
                    boxes[v_line[index][3]][2] = int(np.average(x_set))
                else:
                    raise ValueError

        merge_v_line_list = np.array(merge_v_line_list, dtype=np.int)
        for index_, box_ in enumerate(boxes):
            if box_[0] > box_[2]:
                boxes[index_][0] = box_[2]
                boxes[index_][2] = box_[0]
            if box_[1] > box_[3]:
                boxes[index_][1] = box_[3]
                boxes[index_][3] = box_[1]

        return merge_v_line_list, boxes

    def merge_line(self, boxes, iou_threshold=-0.1, distance_threshold='calculate'):
        """
        image:
            这个是经过检测从原图抠出来的patch
        boxes：
            格式为[[x0, y0, x1, y1],……]，即左上右下，是相对于抠出来patch的坐标位置
        iou_threshold：
            iou即把横线移到同一水平后的交并比（把竖线移到竖方向同一位置后的交并比），
            两条线iou小于阈值可合并（需同时满足distance_threshold）。
            eg：
                calculate：表示需要通过cell的height基础出阈值。
                20：表示直接给出阈值，不需要计算。
        distance_threshold：
            横线是两条线y的距离相对图像h的比例阈值（竖线是两条线x的距离相对图像h的比例阈值，比例要和横线保持一致，所以也用h），
            两条小距离小于阈值可合并（需同时满足iou_threshold）
        show_flag：
            是否显示图片演示
        """
        # boxes = self.fill_table(image, boxes)
        # start_time = time.time()
        h_line = []
        v_line = []
        index = 0
        for box in boxes:
            if abs(box[0] - box[2]) > 0: h_line.append([[box[0], box[1]], [box[2], box[1]], ['up'], index])
            if abs(box[0] - box[2]) > 0: h_line.append([[box[0], box[3]], [box[2], box[3]], ['down'], index])
            if abs(box[1] - box[3]) > 0: v_line.append([[box[0], box[1]], [box[0], box[3]], ['left'], index])
            if abs(box[1] - box[3]) > 0: v_line.append([[box[2], box[1]], [box[2], box[3]], ['right'], index])
            index += 1
        if distance_threshold == 'calculate':
            distance_threshold = self.calculate_distance_threshold(boxes)
        else:
            distance_threshold = np.float(distance_threshold)

        merge_h_line_list, boxes = self.merge_h_lines(h_line, iou_threshold, distance_threshold, boxes)
        merge_v_line_list, boxes = self.merge_v_lines(v_line, iou_threshold, distance_threshold, boxes)

        for box in copy.deepcopy(boxes):
            if abs(box[0] - box[2]) < 3 or abs(box[1] - box[3]) < 3 or abs(box[0] - box[2]) * abs(box[1] - box[3]) < 9:
                boxes.remove(box)

        return merge_h_line_list, merge_v_line_list, boxes

    def remove_duplicate(self, boxes, table_h, table_w):
        # start_time = time.time()
        show_box = np.ones((table_h, table_w, 3), dtype=np.uint8) * 255
        remove_dup_boxes = []
        for index_one in range(len(boxes)):
            for index_two in range(len(boxes)):
                if index_two > index_one:
                    iou, adjust_flag = self.cal_iou(boxes[index_one].copy(), boxes[index_two].copy())
                    if adjust_flag:
                        min_x = min(boxes[index_one][0], boxes[index_one][2], boxes[index_two][0], boxes[index_two][2])
                        max_x = max(boxes[index_one][0], boxes[index_one][2], boxes[index_two][0], boxes[index_two][2])
                        min_y = min(boxes[index_one][1], boxes[index_one][3], boxes[index_two][1], boxes[index_two][3])
                        max_y = max(boxes[index_one][1], boxes[index_one][3], boxes[index_two][1], boxes[index_two][3])
                        h, w = max_y - min_y, max_x - min_x
                        mask_img = np.zeros((h, w))
                        mask_img[boxes[index_one][1] - min_y:boxes[index_one][3] - min_y, boxes[index_one][0] - min_x:boxes[index_one][2] - min_x] += 1
                        mask_img[boxes[index_two][1] - min_y:boxes[index_two][3] - min_y, boxes[index_two][0] - min_x:boxes[index_two][2] - min_x] += 1
                        mask_img[mask_img < 2] = 0
                        overlap_area_index = np.argwhere(mask_img == 2)
                        overlap_area_min_x = min(overlap_area_index[:, 1])
                        overlap_area_max_x = max(overlap_area_index[:, 1])
                        overlap_area_min_y = min(overlap_area_index[:, 0])
                        overlap_area_max_y = max(overlap_area_index[:, 0])

                        point_x_list = [boxes[index_one][0] - min_x, boxes[index_one][2] - min_x,
                                        overlap_area_min_x, overlap_area_max_x]
                        point_y_list = [boxes[index_one][1] - min_y, boxes[index_one][3] - min_y,
                                        overlap_area_min_y, overlap_area_max_y]
                        point_list = []
                        for one in point_x_list:
                            for two in point_y_list:
                                point_list.append([one, two])
                        point_list = np.unique(point_list, axis=0)

                        max_box = []
                        max_box_area = -1
                        for one in range(len(point_list)):
                            for two in range(len(point_list)):
                                if two <= one:
                                    continue
                                x_0 = min(point_list[one][0], point_list[two][0])+1
                                y_0 = min(point_list[one][1], point_list[two][1])+1
                                x_1 = max(point_list[one][0], point_list[two][0])-1
                                y_1 = max(point_list[one][1], point_list[two][1])-1
                                if np.sum(mask_img[y_0:y_1, x_0:x_1]) < 10:
                                    box_area = abs(x_1-x_0)*abs(y_1-y_0)
                                    if max_box_area < box_area:
                                        max_box_area = box_area
                                        max_box = [min(x_0+min_x, x_1+min_x),
                                                   min(y_0+min_y, y_1+min_y),
                                                   max(x_0+min_x, x_1+min_x),
                                                   max(y_0+min_y, y_1+min_y)]
                        boxes[index_one] = max_box
            remove_dup_boxes.append(boxes[index_one])
        # print('remove dup boxes use time: ', time.time()-start_time)
        # for box in remove_dup_boxes:
        #     cv2.rectangle(show_box, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
        # cv2.imshow('image', show_box)
        # cv2.waitKey()
        return remove_dup_boxes

    def fill_table(self, boxes):
        if len(boxes) == 0:
            return boxes
        x_set, y_set = [], []
        for box in boxes:
            x_set.append(box[0])
            x_set.append(box[2])
            y_set.append(box[1])
            y_set.append(box[3])

        table_min_x = min(x_set)
        table_max_x = max(x_set)
        table_min_y = min(y_set)
        table_max_y = max(y_set)
        image_binary = np.ones((table_max_y-table_min_y, table_max_x-table_min_x), dtype=np.uint8)*255
        offset_boxes = []
        for box in boxes:
            offset_boxes.append([box[0]-table_min_x, box[1]-table_min_y, box[2]-table_min_x, box[3]-table_min_y])
        remove_dup_boxes = self.remove_duplicate(offset_boxes, table_max_y - table_min_y, table_max_x - table_min_x)
        boxes = []
        for box in remove_dup_boxes:
            boxes.append([box[0] + table_min_x, box[1] + table_min_y, box[2] + table_min_x, box[3] + table_min_y])
        for box in remove_dup_boxes:
            image_binary[box[1]:box[3], box[0]:box[2]] = 0

        # start_time = time.time()
        new_box = []
        h, w = np.shape(image_binary)[0], np.shape(image_binary)[1]

        i, j = 0, 0
        row_block = 1
        for _ in range(h):
            if not np.sum(image_binary[j:min(j + row_block, h), :]):
                i = 0
                j = min(j + row_block, h)
                continue
            for _ in range(w):
                if image_binary[j, i]:
                    step_x = 0
                    step_y = 0
                    for ii in range(i, w):
                        if image_binary[j, ii]:
                            step_x += 1
                        else:
                            break
                    for jj in range(j, h):
                        if np.average(image_binary[jj, i:i+step_x]) == 255:
                            step_y += 1
                        else:
                            break
                    # print(i, j, step_x, step_y)
                    image_binary[j:j+step_y, i:i+step_x] = 0
                    new_box.append([i, j, i+step_x, j+step_y])
                i += 1
                if i >= w:
                    i = 0
                    break
            j += 1
            if j >= h:
                break

        # print('use time fill: ', time.time()-start_time)

        new_box_reoffset = []
        for box in new_box:
            new_box_reoffset.append([box[0] + table_min_x, box[1] + table_min_y, box[2] + table_min_x, box[3] + table_min_y])

        boxes = boxes + new_box_reoffset
        return boxes

    def table_structure(self, boxes, text_list, out_dir=None):
        """

        :param boxes: [[left_up_x, left_up_y, right_down_x, right_down_y], ……]
        :param text_list: ['hello', 'world', ……]
        :param out_dir: 生成html的输出位置
        :return:
        """
        # merge -> start
        _, _, merge_boxes = \
            self.merge_line(copy.deepcopy(boxes),
                            iou_threshold=-0.1,
                            distance_threshold='calculate'
                            )  # 0.025

        fill_boxes = self.fill_table(copy.deepcopy(merge_boxes))
        _, _, merge_boxes = \
            self.merge_line(copy.deepcopy(fill_boxes),
                            iou_threshold=-np.inf,  # -0.1,
                            distance_threshold='calculate'
                            )

        iou_matrix = \
            self.cal_iou_parallel(
                torch.tensor(
                    merge_boxes, dtype=torch.float32,
                    device='cuda:0' if torch.cuda.is_available() else 'cpu'
                ),
                torch.tensor(
                    boxes, dtype=torch.float32,
                    device='cuda:0' if torch.cuda.is_available() else 'cpu'
                ),
                cal_type=0
            ).cpu().numpy()
        new_idx = np.argmax(iou_matrix, axis=0).tolist()
        boxes, text_list = merge_boxes, np.array(text_list)[new_idx].tolist()
        if len(boxes) != len(text_list):
            raise ValueError
        # merge -> end

        # 按照x0，y0，x1，y1的顺序进行排序，如果要给box排序的话取消注释，但是没有把握尽量不要排序，因为可能影响后边的text和box的对应关系
        text_list = np.array(text_list)
        boxes = np.array([[box[1], box[0], box[3], box[2]] for box in boxes])
        temp_boxes = np.transpose(boxes)
        temp_boxes = np.flipud(temp_boxes)
        sort_index = np.lexsort(temp_boxes)
        boxes = boxes[sort_index]
        text_list = text_list[sort_index]
        boxes = [[box[1], box[0], box[3], box[2]] for box in boxes]
        boxes, text_list = list(boxes), list(text_list)

        x_set, y_set = [], []
        for box in boxes:
            x_set.append(box[0])
            x_set.append(box[2])
            y_set.append(box[1])
            y_set.append(box[3])
        table_min_x, table_max_x, table_min_y, table_max_y = min(x_set), max(x_set), min(y_set), max(y_set)
        offset_boxes = []
        w_list, h_list = [], []
        for box in boxes:
            offset_boxes.append(
                [box[0] - table_min_x, box[1] - table_min_y, box[2] - table_min_x, box[3] - table_min_y])
            w_list.append(abs((box[0] - table_min_x) - (box[2] - table_min_x)))
            h_list.append(abs((box[1] - table_min_y) - (box[3] - table_min_y)))
        scale = min(min(w_list), min(h_list))
        h, w = table_max_y-table_min_y+1, table_max_x-table_min_x+1

        # txt cell坐标点
        x_point_dict, y_point_dict = self.cell_num_type(offset_boxes, scale)
        txt_cell_coordinate_list = {}
        for index, box in enumerate(offset_boxes):
            x_0, y_0, x_1, y_1 = \
                x_point_dict[box[0] // scale], \
                y_point_dict[box[1] // scale], \
                x_point_dict[box[2] // scale], \
                y_point_dict[box[3] // scale]
            txt_cell_coordinate_list[index] = [[y_0, x_0, y_1, x_1]]
            txt_cell_coordinate_list[index].append(text_list[index].replace('<***۞Enter۞***>', ''))

        if out_dir:
            # '''写入excel和word的代码，需要的话取消注释
            f = xlsxwriter.Workbook(out_dir.replace('.html', '.xlsx'))  # 创建excel文件
            worksheet1 = f.add_worksheet('sheet1')
            # color_list = ['#FFB6C1', '#FFC0CB', '#DC143C','#FFF0F5','#DB7093','#FF69B4','#FF1493','#C71585' ,'#DA70D6','#D8BFD8','#DDA0DD','#EE82EE','#FF00FF','#FF00FF','#8B008B','#800080','#BA55D3','#9400D3']
            color_list = ['#FFFFFF']

            cell_max_idx_x = x_point_dict[max(x_point_dict.keys())]
            cell_max_idx_y = y_point_dict[max(y_point_dict.keys())]
            None_list = [None for i in range(cell_max_idx_x)]
            for i in range(cell_max_idx_y):
                worksheet1.write_row(i, 0, None_list, f.add_format({'fg_color': '#FFFFFF', 'border': 2}))
            # worksheet1.set_column(0, w*10, 1)
            [worksheet1.set_column(i, 1) for i in range(cell_max_idx_x)]
            [worksheet1.set_row(i, 20) for i in range(cell_max_idx_y)]
            # box_file = open('/Volumes/my_disk/company/sensedeal/buffer_disk/buffer_8/1.txt', 'a+')
            index = 0
            for box in offset_boxes:
                worksheet1.write(y_point_dict[box[1] // scale], x_point_dict[box[0] // scale],
                                 text_list[index].replace('<***۞Enter۞***>', '\n'),
                                 f.add_format({'fg_color': color_list[np.random.randint(0, len(color_list))], 'border': 2, 'text_wrap': 1}))
                if y_point_dict[box[1] // scale] != y_point_dict[box[3] // scale]-1 or \
                        x_point_dict[box[0] // scale] != x_point_dict[box[2] // scale]-1:
                    worksheet1.merge_range(y_point_dict[box[1] // scale], x_point_dict[box[0] // scale],
                                           y_point_dict[box[3] // scale]-1, x_point_dict[box[2] // scale]-1,
                                           text_list[index].replace('<***۞Enter۞***>', '\n'),
                                           f.add_format({'fg_color': color_list[np.random.randint(0, len(color_list))], 'border': 2, 'text_wrap': 1}))
                index += 1
                # box_file.write(' '.join([str(i) for i in box]) + '\n')
            f.close()

            # 写入word开始
            # doc = Document()
            # table = doc.add_table(cell_max_idx_y, cell_max_idx_x, style='Table Grid')
            #
            # index = 0
            # for box in offset_boxes:
            #     table.cell(y_point_dict[box[1] // scale], x_point_dict[box[0] // scale]).merge(table.cell(y_point_dict[box[3] // scale] - 1, x_point_dict[box[2] // scale] - 1)).text = text_list[index].replace('<***۞Enter۞***>', '<br>')
            #     index += 1
            # doc.save(out_path.replace('.html', '.docx'))
            # '''

            # '''
            # 写入html开始
            html_table_list = []
            for i in range(1 if h // scale == 0 else h // scale):
                html_h_list = []
                for j in range(1 if w // scale == 0 else w // scale):
                    html_h_list.append('')
                html_table_list.append(html_h_list)

            index = 0
            for box in offset_boxes:
                # x_0, y_0, x_1, y_1 = box[0] // scale, box[1] // scale, box[2] // scale, box[3] // scale
                x_0, y_0, x_1, y_1 = \
                    x_point_dict[box[0] // scale], \
                    y_point_dict[box[1] // scale], \
                    x_point_dict[box[2] // scale], \
                    y_point_dict[box[3] // scale]
                cell_str = '<td '
                cell_str = cell_str + 'class=' + '"' + 'tg-0lax' + '" '
                cell_str = cell_str + 'rowspan=' + '"' + str(y_1 - y_0) + '" '  # 向下融合cell的数量
                cell_str = cell_str + 'colspan=' + '"' + str(x_1 - x_0) + '" '  # 向右融合cell的数量
                cell_str = cell_str + 'height=' + '"' + str(box[3] - box[1]) + '" '  # 设置cell的宽
                cell_str = cell_str + 'width=' + '"' + str(box[2] - box[0]) + '" '  # 设置cell的高
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

    def cell_num_type(self, offset_boxes, scale):
        '''
        输入的是融合的box占了多少最小单元，但是实际标记的时候只需要告诉客户box的个数，而不需要知道融合了多少个最小单元。
        所以这个函数进一步处理，得到计数方式的cell的左上角右下角
        :return: 计数方式的cell的左上角右下角
        '''
        x_point_list = []
        y_point_list = []
        for index, box in enumerate(offset_boxes):
            x_point_list.append(box[0] // scale)
            x_point_list.append(box[2] // scale)
            y_point_list.append(box[1] // scale)
            y_point_list.append(box[3] // scale)
        x_point_list, y_point_list = sorted(list(set(x_point_list))), sorted(list(set(y_point_list)))
        x_point_dict = {j: i for i, j in enumerate(x_point_list)}
        y_point_dict = {j: i for i, j in enumerate(y_point_list)}
        return x_point_dict, y_point_dict

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
    # boxes = [[0, 0, 30, 30], [30, 0, 60, 30], [0, 30, 30, 60], [30, 30, 60, 60]]
    boxes = [[0, 0, 30, 30], [30, 0, 60, 30], [0, 30, 30, 60], [30, 30, 60, 60]]
    text_list = ['1', '2', '3', '4']

    TS = TableStructure()
    TS.table_structure(boxes, text_list, './a.html')
