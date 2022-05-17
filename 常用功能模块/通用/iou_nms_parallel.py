import os
import numpy as np
import torch
import torchvision
import time


def torch_box_iou(boxes_0, boxes_1, cal_type=-1):
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


def torch_nms(boxes, scores, iou_threshold):
    keep = []  # 最终保留的结果， 在boxes中对应的索引；
    idxs = scores.argsort()  # 值从小到大的 索引
    while idxs.numel() > 0:  # 循环直到null； numel()： 数组元素个数
        # 得分最大框对应的索引, 以及对应的坐标
        max_score_index = idxs[-1]
        max_score_box = boxes[max_score_index][None, :]  # [1, 4]
        keep.append(max_score_index)
        if idxs.size(0) == 1:  # 就剩余一个框了；
            break
        idxs = idxs[:-1]  # 将得分最大框 从索引中删除； 剩余索引对应的框 和 得分最大框 计算IoU；
        other_boxes = boxes[idxs]  # [?, 4]
        ious = torch_box_iou(max_score_box, other_boxes)  # 一个框和其余框比较 1XM
        idxs = idxs[ious[0] <= iou_threshold]
    keep = idxs.new(keep)  # Tensor
    return keep


def numpy_box_iou(boxes_0, boxes_1, cal_type=-1):
    """
    NxM， boxes_0中每个框和boxes_1中每个框的IoU值；
    :param boxes_0: [[x_0, y_0, x_1, y_1], ……]，左上右右下角，N个
    :param boxes_1: [[x_0, y_0, x_1, y_1], ……]，左上右右下角，M个
    :return:
    """
    area_0 = (boxes_0[:, 2] - boxes_0[:, 0]) * (boxes_0[:, 3] - boxes_0[:, 1])  # 每个框的面积 (N,)
    area_1 = (boxes_1[:, 2] - boxes_1[:, 0]) * (boxes_1[:, 3] - boxes_1[:, 1])  # 每个框的面积 (M,)

    # broadcasting, 两个数组各维度大小从后往前对比一致、或者有一维度值为1、或者有一维度为None；
    lt = np.maximum(boxes_0[:, np.newaxis, :2], boxes_1[:, :2])
    rb = np.minimum(boxes_0[:, np.newaxis, 2:], boxes_1[:, 2:])

    wh = rb - lt
    wh = np.maximum(0, wh)  # [N, M, 2]
    inter = wh[:, :, 0] * wh[:, :, 1]

    if cal_type == -1:
        iou = inter / (area_0[:, np.newaxis] + area_1 - inter)
    elif cal_type == 0:
        iou = inter / (area_0[:, np.newaxis] + np.zeros(area_1.shape[0], dtype=np.float32))
    elif cal_type == 1:
        iou = inter / (torch.zeros(area_0.shape[0], dtype=np.float32)[:, np.newaxis] + area_1)
    else:
        raise ValueError
    return iou  # NxM


def numpy_nms(boxes, scores, iou_threshold):
    idxs = scores.argsort()  # 按分数 降序排列的索引 [N]
    keep = []
    while idxs.size > 0:  # 统计数组中元素的个数
        max_score_index = idxs[-1]
        max_score_box = boxes[max_score_index][None, :]
        keep.append(max_score_index)
        if idxs.size == 1:
            break
        idxs = idxs[:-1]  # 将得分最大框 从索引中删除； 剩余索引对应的框 和 得分最大框 计算IoU；
        other_boxes = boxes[idxs]  # [?, 4]
        ious = numpy_box_iou(max_score_box, other_boxes)  # 一个框和其余框比较 1XM
        idxs = idxs[ious[0] <= iou_threshold]
    keep = np.array(keep)
    return keep


if __name__ == '__main__':
    print('↓')
    for i in range(20):
        # iou
        # boxes = np.array([[0, 0, 100, 100]] * 2000)
        # # boxes = np.array([[0, 0, 100, 100], [0, 0, 100, 79], [2, 5, 12, 655], [1000, 1000, 1200, 1200]])
        # start = time.time()
        #
        # # boxes_ = torch.tensor(boxes, dtype=torch.float32, device='cuda:0')
        # # boxes_ = torch.tensor(boxes, dtype=torch.float32, device='cpu')
        # # tv_iou_matrix = torchvision.ops.box_iou(boxes_, boxes_).cpu().numpy()
        # # to_iou_matrix = torch_box_iou(boxes_, boxes_).cpu().numpy()
        # numpy_iou_matrix = numpy_box_iou(boxes, boxes)
        #
        # print('use time: ', time.time() - start)

        # nms
        # boxes = np.array([[0, 0, 100, 100], [0, 0, 100, 100]]*1000)
        # scores = np.array([1.0, 0.9]*1000)
        boxes = np.array([[0, 0, 100, 100], [0, 0, 100, 90], [0, 0, 50, 50]])
        scores = np.array([1.0, 0.9, 0.8])
        start = time.time()

        tv_keeps = torchvision.ops.nms(torch.tensor(boxes, dtype=torch.float32), torch.tensor(scores, dtype=torch.float32), 0.8).cpu().numpy()
        to_keeps = torch_nms(torch.tensor(boxes), torch.tensor(scores), 0.8).cpu().numpy()
        numpy_keeps = numpy_nms(boxes, scores, 0.8)

        print('use time: ', time.time() - start)
